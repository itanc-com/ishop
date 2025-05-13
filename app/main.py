from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.exceptions.app_exceptions import AppBaseException
from app.db.base import Base, engine
from app.modules.auth.routers import router as auth_router
from app.modules.category.models import Category  # noqa
from app.modules.product.models import Product  # noqa
from app.modules.product.routers import router as products_router
from app.modules.user.models import User  # noqa
from app.modules.user.routers import router as user_router

app = FastAPI(
    title="IShop API",
    description="API for IShop, a headless e-commerce application.",
)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the IShop API!"}


app.include_router(products_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.exception_handler(AppBaseException)
async def handle_app_exception(request: Request, exc: AppBaseException):
    error_model = exc.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": error_model.model_dump(mode="json")},  
    )
