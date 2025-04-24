from fastapi import FastAPI

from category import Category  # noqa
from db.base import Base, engine
from product import Product  # noqa
from user import User  # noqa

app = FastAPI(
    title="IShop API",
    description="API for IShop, a headless e-commerce application.",
)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the IShop API!"}
