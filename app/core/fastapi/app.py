from fastapi import FastAPI

from app.core.fastapi.app_lifespan import lifespan
from app.core.pydantic.settings import EnvironmentType, settings

app: FastAPI = FastAPI(
    title="IShop API",
    description="API for iShop, a headless e-commerce application.",
    version="1.0.0",
    docs_url=None if settings.environment == EnvironmentType.PRODUCTION else "/docs",
    redoc_url=None if settings.environment == EnvironmentType.PRODUCTION else "/redoc",
    # dependencies=[Depends(Logging)],
    # middleware=make_middleware(),
    lifespan=lifespan,
)

