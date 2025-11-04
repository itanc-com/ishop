from datetime import datetime

from pydantic import BaseModel, Field

from app.common.schemas.pagination import PaginationInfo


class ProductBase(BaseModel):
    category_id: int = Field(..., example=1)
    title: str = Field(..., max_length=255, example="Super Comfortable Chair")
    description: str = Field(..., example="A modern, ergonomic chair perfect for long working hours.")
    sku: str = Field(..., example="CHAIR-1234")
    price: float = Field(default=0.0, ge=0, example=99.99)
    is_available: bool = Field(default=False)
    is_visible: bool = Field(default=False)


class ProductInCreate(ProductBase):
    """
    Used for creating a new product.
    Does not include `id` or timestamps.
    """

    pass


class ProductInUpdate(ProductBase):
    """
    Used for updating a product.
    Typically, the `id` is passed via path param, not the schema body.
    """

    pass


class ProductOutRead(ProductBase):
    """
    Used for reading product data.
    Includes `id`, `date_created`, and `date_modified`.
    """

    id: int = Field(..., description="Product unique identifier", examples=[1])

    date_created: datetime = Field(
        ...,
        description="Timestamp when the product was created",
        examples=["2023-01-01T00:00:00"],
    )
    date_modified: datetime = Field(
        ...,
        description="Timestamp when the product was last updated",
        examples=["2023-01-01T12:30:00"],
    )

    model_config = {"from_attributes": True}


class ProductOutList(BaseModel):
    """
    Used for listing products with pagination support.
    Contains a list of ProductOutRead items and pagination metadata.
    """

    items: list[ProductOutRead] = Field(..., description="List of products")
    pagination: PaginationInfo = Field(..., description="Pagination information")

    model_config = {"from_attributes": True}
