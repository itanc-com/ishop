from fastapi import FastAPI

from db.base import Base, engine
from user import User  # noqa

app = FastAPI(
    title="IShop API",
    description="API for IShop, a headless e-commerce application.",
)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the IShop API!"}
