from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # App runs between this and the end

    # Shutdown
    await sessionmanager.close()
