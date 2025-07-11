from datetime import datetime

from pydantic import BaseModel, Field


class CartItemBase(BaseModel):
    user_id: int = Field(..., example=1, description="internal id for the user")
    product_id: int = Field(..., example=123, description="internal id for the product")
    quantity: int = Field(..., gt=0, example=2, description="Quantity of items")


class CartItemRead(CartItemBase):
    title: str = Field(..., example="Super Comfortable Chair", description="Product title")
    sku: str = Field(..., example="ABC-1234", description="Product SKU (Stock Keeping Unit)")
    price: float = Field(default=0.0, ge=0, example=99.99, description="Price per item")
    total: float = Field(default=0.0, ge=0, example=199.98, description="Total price for this item based on quantity")
    date_created_gmt: datetime | None = Field(default=None, description="Creation date")
    date_modified_gmt: datetime | None = Field(default=None, description="Last modified date")


class CartItemCreate(CartItemBase):
    """
    Used for creating a new cart item.
    Does not include `id` or timestamps.
    """

    pass


class CartBulkCreate(BaseModel):
    """
    this should be used for bulk creation of cart items.
    It can accept a list of CartItemCreate schemas.
    """

    items: list[CartItemCreate] = Field(..., description="List of cart items to create")


class CartItemQuantityUpdate(CartItemBase):
    """
    Used for updating a cart item quantity.
    """

    pass


class CartRead(BaseModel):
    """
    Represents list of all cart items with additional fields.
    It can be used to read cart items.
    """

    items: list[CartItemRead] = Field(..., description="List of cart items to read")
