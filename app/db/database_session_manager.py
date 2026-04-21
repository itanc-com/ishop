import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseNotInitializedError(RuntimeError):
    """Raised when DatabaseSessionManager is used after close()."""


class DatabaseSessionManager:
    """Owns the async engine and sessionmaker.

    Has no opinion about transaction boundaries — the caller decides
    when to `begin()`, `commit()`, or `rollback()`. The only cleanup
    guarantee is that the underlying session/connection is closed
    (returned to the pool) when the context manager exits.
    """

    _engine: AsyncEngine | None
    _sessionmaker: async_sessionmaker[AsyncSession] | None

    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        self._engine = create_async_engine(host, **(engine_kwargs or {}))
        self._sessionmaker = async_sessionmaker(expire_on_commit=False, bind=self._engine)

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseNotInitializedError("DatabaseSessionManager is closed")
        async with self._engine.connect() as connection:
            yield connection

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseNotInitializedError("DatabaseSessionManager is closed")
        session = self._sessionmaker()
        try:
            yield session
        finally:
            await session.close()
