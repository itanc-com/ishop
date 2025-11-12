from datetime import datetime

from pydantic import BaseModel


# Data from JOIN, aggregation, or transformation (not matching a single table)
class CartItemDTO(BaseModel):
    """
    Data Transfer Object for cart items with product details.
    Used internally between repository and usecase layers.

    Combines data from:
    - cart_items: user_id, product_id, quantity, price_cart, total, dates
    - products: title, sku, price_product
    """

    user_id: int
    product_id: int
    quantity: int
    price_cart: float  # Only this price
    subtotal: float
    date_created: datetime
    date_modified: datetime
    title: str
    sku: str
    price_product: float
    is_available: bool = False  # if product is available in catalog

    class Config:
        from_attributes = True  # Allows model_validate() from SQLAlchemy objects


class CartItemSyncDTO(BaseModel):
    """
    Data Transfer Object for cart item synchronization.
    Used internally between repository and usecase layers.
    """

    product_id: int
    title: str
    sku: str
    price_product: float
    is_available: bool = True
    is_updated: bool = True

    class Config:
        from_attributes = True
