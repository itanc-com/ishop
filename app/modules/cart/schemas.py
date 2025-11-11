from datetime import datetime

from pydantic import BaseModel, Field


# A cart represents a user's shopping cart,
# with each record linking a user, a product, and the desired quantity.
class CartItemBase(BaseModel):
    product_id: int = Field(..., json_schema_extra={"examples": [123], "description": "internal id for the product"})
    quantity: int = Field(..., gt=0, json_schema_extra={"examples": [2], "description": "Quantity of items"})


class CartItemOutRead(CartItemBase):
    title: str = Field(..., json_schema_extra={"examples": ["Super Comfortable Chair"], "description": "Product title"})
    sku: str = Field(
        ..., json_schema_extra={"examples": ["ABC-1234"], "description": "Product SKU (Stock Keeping Unit)"}
    )
    price: float = Field(default=0.0, ge=0, examples=[99.99], description="Price per item")
    subtotal: float = Field(
        default=0.0, ge=0, examples=[199.98], description="Total price for this item based on quantity"
    )
    is_available: bool = Field(default=True, description="Indicates if the product is currently available in stock")
    date_created_gmt: datetime | None = Field(default=None, description="Creation date")
    date_modified_gmt: datetime | None = Field(default=None, description="Last modified date")


class CartItemInCreate(CartItemBase):
    """
    Schema for creating a single cart item.
    """

    pass


class CartInCreate(BaseModel):
    """
    this should be used for bulk creation of cart items.
    It can accept a list of CartInCreate schemas.
    """

    items: list[CartItemInCreate] = Field(..., description="List of cart items to bulk create a new cart")


class CartItemInUpdate(BaseModel):
    """
    Used for updating a cart item quantity.
    """

    product_id: int = Field(..., json_schema_extra={"examples": [123], "description": "internal id for the product"})
    quantity: int = Field(..., ge=0, json_schema_extra={"examples": [2], "description": "Quantity of items"})


class CartOutRead(BaseModel):
    """
    Represents list of all cart items with additional fields.
    It can be used to read cart items.
    """

    total: float = Field(default=0.0, ge=0, examples=[299.98], description="Total price of all items in the cart")
    items: list[CartItemOutRead] = Field(..., description="List of cart items to read")
