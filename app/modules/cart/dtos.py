from datetime import datetime

from pydantic import BaseModel, Field


class CartItemWithProductDTO(BaseModel):
    """
    Data Transfer Object for cart items with product details.
    Used internally between repository and usecase layers.

    Combines data from:
    - cart_items: user_id, product_id, quantity, price_cart, total, dates
    - products: title, sku, price_product
    """

    # Cart item fields (from cart_items)
    user_id: int = Field(..., description="User ID who owns the cart item")
    product_id: int = Field(..., description="Product ID in the cart")
    quantity: int = Field(..., gt=0, description="Quantity of the product")
    price_cart: float = Field(..., ge=0, description="Price per item when added to cart (from cart_items)")
    total: float = Field(..., ge=0, description="Total price (price_cart * quantity)")
    date_created: datetime = Field(..., description="When the cart item was created")
    date_modified: datetime = Field(..., description="When the cart item was last modified")

    # Product fields (from products via JOIN)
    title: str = Field(..., description="Product title (current)")
    sku: str = Field(..., description="Product SKU (current)")
    price_product: float = Field(..., ge=0, description="Current product price (from products)")

    class Config:
        from_attributes = True  # Allows model_validate() from SQLAlchemy objects
