from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field
from schemas import  ProductInsert, ProductUpdate, ProductView
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductInsert):
 #... compelete this router 
 
    # Return Product ID 
    return {"message": "Product created successfully"}


@router.get("/{product_id}", response_model=ProductView)
def get_product(product_id: int):
    #... complete this router
    ## Return Product
    return {"message": "Product retrieved successfully", "product": product}
    return {"message": "Product not found"}, status.HTTP_404_NOT_FOUND


@router.put("/{product_id}", response_model=ProductView)
def update_product(product_id: int, product: ProductUpdate):
    #... complete this router
    return {"message": "Product updated successfully", "product": updated_product}
    return {"message": "Product not found"}, status.HTTP_404_NOT_FOUND


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    #... complete this router
    return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}, status.HTTP_404_NOT_FOUND
