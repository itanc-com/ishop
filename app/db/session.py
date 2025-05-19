from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pydantic.settings import settings

from .database_session_manager import DatabaseSessionManager

if settings.environment != "production":
    settings.echo_sql = True

engine_options = {
    "echo": settings.echo_sql,
    "connect_args": {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
}

sessionmanager = DatabaseSessionManager(settings.database_url, engine_options)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
