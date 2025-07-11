from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

from app.core.fastapi.app_state import AppStates, set_app_state
from app.db.base import Base
from app.db.session import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_app_state(app, AppStates.APP_START_TIME, datetime.now(timezone.utc).replace(microsecond=0))

    # Startup
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # App runs between this and the end

    # Shutdown
    await sessionmanager.close()
