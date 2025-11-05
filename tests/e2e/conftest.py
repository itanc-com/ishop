import asyncio
import logging

from tests.e2e.global_setup import clear_database

pytest_plugins = [
    "tests.e2e.fixtures.fxt_base",
    "tests.e2e.fixtures.users",
    "tests.e2e.fixtures.category",
]


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and configured.
    This runs before any test collection or execution.
    """
    print("Setting up test environment...")

    # Run async function from sync context
    try:
        # Create a new event loop for the async operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(clear_database())
        loop.close()
    except Exception as e:
        print(f"Failed to clear database: {e}")
        raise

    print("Test environment ready!")


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
