from fastapi import FastAPI

from src.db.base import Base, engine
from src.modules.category.models import Category  # noqa
from src.modules.product.models import Product  # noqa
from src.modules.product.routers import router as products_router
from src.modules.user.models import User  # noqa

app = FastAPI(
    title="IShop API",
    description="API for IShop, a headless e-commerce application.",
)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the IShop API!"}


app.include_router(products_router)
