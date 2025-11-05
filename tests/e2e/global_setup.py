from sqlalchemy import text

from app.core.logger.config import configure_logger
from app.core.logger.get_logger import ServiceName, get_logger
from app.db.session import sessionmanager

# Configure logging for tests
configure_logger()

logger = get_logger(service=ServiceName.E2E_TEST_SERVICE)


async def clear_database():
    """
    Clear all data from the database tables for clean test environment.

    This method truncates all tables to ensure each test run starts with a clean state.
    It preserves table structure while removing all data.
    """
    async with sessionmanager.session() as session:
        try:
            # Get all table names from the database
            result = await session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            )
            tables = result.fetchall()

            if not tables:
                logger.info("No tables found to clear")
                return

            logger.debug(f"Found {len(tables)} tables to clear: {[t[0] for t in tables]}")

            # Disable foreign key constraints temporarily
            await session.execute(text("PRAGMA foreign_keys = OFF"))

            # Clear all tables
            for table in tables:
                table_name = table[0]
                await session.execute(text(f"DELETE FROM {table_name}"))
                logger.info(f"Cleared table: {table_name}")

            # Reset auto-increment counters only if sqlite_sequence table exists
            sequence_check = await session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
            )
            if sequence_check.fetchone():
                logger.info("sqlite_sequence table found, resetting auto-increment counters...")
                # Delete sequences for all tables (DELETE succeeds even if row doesn't exist)
                for table in tables:
                    table_name = table[0]
                    await session.execute(
                        text("DELETE FROM sqlite_sequence WHERE name=:table_name"), {"table_name": table_name}
                    )
                    logger.info(f"Reset sequence for: {table_name}")
            else:
                logger.info("No sqlite_sequence table found, skipping sequence reset")

            # Re-enable foreign key constraints
            await session.execute(text("PRAGMA foreign_keys = ON"))

            await session.commit()
            logger.info("Database cleared successfully")

        except Exception as e:
            await session.rollback()
            logger.error(f"Error clearing database: {e}")
            raise
