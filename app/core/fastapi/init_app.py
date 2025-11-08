from fastapi import FastAPI

from app.core.config.settings import settings
from app.core.fastapi.app import app
from app.core.fastapi.exception_handlers import register_exception_handlers
from app.core.fastapi.routers import router_v1
from app.core.logger.config import configure_logger
from app.core.middelware.middelware_setup import setup_middlewares
from app.utils.date_time import get_utc_now

from .app_state import AppStates, get_app_state


@app.get("/")
async def root() -> dict:
    return {
        "name": "iShop API",
        "version": "1.0.0",
        "status": "OK",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_status() -> dict:
    return {
        "status": "OK",
        "uptime": str(get_utc_now() - get_app_state(app, AppStates.APP_START_TIME)),
    }


def init_app() -> FastAPI:
    configure_logger()
    app.include_router(router_v1)
    setup_middlewares(app)
    register_exception_handlers(app)
    return app
