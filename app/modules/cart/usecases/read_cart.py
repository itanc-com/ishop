from sqlalchemy.exc import SQLAlchemyError

from app.common.exceptions.app_exceptions import DatabaseOperationException
from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartItemRead, CartRead


class ReadCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int) -> CartRead | None:
        try:
            cart_items = await self.cart_item_repository.find_all(user_id)
        except SQLAlchemyError as e:
            raise DatabaseOperationException(operation="read", message=str(e), data={"user_id": user_id})

        items_read: list[CartItemRead] = [
            CartItemRead(
                user_id=cart_item.user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                title=getattr(cart_item, "title", ""),
                sku=getattr(cart_item, "sku", ""),
                price=getattr(cart_item, "price", 0.0),
                total=getattr(cart_item, "total", 0.0),
                date_created_gmt=getattr(cart_item, "date_created", None),
                date_modified_gmt=getattr(cart_item, "date_modified", None),
            )
            for cart_item in cart_items
        ]

        return CartRead(items=items_read)
