from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.db.session import get_session

from .repository import ProductRepository
from .schemas import ProductInsert, ProductUpdate, ProductView

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductInsert, session: Annotated[Session, Depends(get_session)]):
    ProductRepository(session).create(product)
    return {"message": "Product created successfully"}


@router.get("/{product_id}", response_model=ProductView)
def get_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product_db = ProductRepository(session).get_by_id(product_id)
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_db


@router.put("/{product_id}", response_model=ProductView)
def update_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    product_db = ProductRepository(session).get_by_id(product_id)
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    updated_product = ProductRepository(session).update(product_db, product)
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product_db = ProductRepository(session).get_by_id(product_id)
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    ProductRepository(session).delete(product_db)
    return {"message": "Product deleted successfully"}
