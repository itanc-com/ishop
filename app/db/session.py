"""Postgres session layer (SQLite allowed for dev/test).

Notes for PgBouncer / Supavisor in transaction-pool mode (e.g. Supabase 6543):
- Prepared statements don't survive connection reuse across clients — set
  `db_statement_cache_size=0` so asyncpg won't cache them.
- Session-level state is unreliable: SET SESSION, LISTEN/NOTIFY,
  session-scoped temp tables, and advisory locks held across
  transactions. Use `SET LOCAL` and transaction-scoped equivalents.
- Let the external pooler handle pooling by turning on
  `db_use_null_pool=True`; SQLAlchemy opens/closes a raw connection per
  checkout and defers reuse to PgBouncer.
- Supabase requires TLS — set `db_ssl="require"` (asyncpg doesn't honor
  libpq's `sslmode` in the URL).
"""
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool

from app.core.config.settings import Settings, settings

from .database_session_manager import DatabaseSessionManager


def _is_postgres(uri: str) -> bool:
    return uri.startswith(("postgresql://", "postgresql+", "postgres://"))


def build_session_manager(settings: Settings) -> DatabaseSessionManager:
    """Build a DatabaseSessionManager from application settings.

    The factory itself is pure — tests that construct their own
    manager via this function do not touch the module-level
    `sessionmanager` singleton below. Postgres-specific engine
    options only apply when the URL is Postgres — SQLite
    (sqlite+aiosqlite://...) gets a minimal config for dev/test.
    """
    engine_options: dict[str, Any] = {"echo": settings.echo_sql}

    if not _is_postgres(settings.database_uri):
        return DatabaseSessionManager(settings.database_uri, engine_options)

    connect_args: dict[str, Any] = {
        "server_settings": {"application_name": settings.db_application_name},
    }
    if settings.db_statement_cache_size is not None:
        connect_args["statement_cache_size"] = settings.db_statement_cache_size
        connect_args["prepared_statement_cache_size"] = settings.db_statement_cache_size
    if settings.db_ssl is not None:
        connect_args["ssl"] = settings.db_ssl

    engine_options["pool_pre_ping"] = settings.db_pool_pre_ping
    engine_options["pool_recycle"] = settings.db_pool_recycle
    engine_options["connect_args"] = connect_args
    if settings.db_use_null_pool:
        engine_options["poolclass"] = NullPool

    return DatabaseSessionManager(settings.database_uri, engine_options)


sessionmanager: DatabaseSessionManager = build_session_manager(settings)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
