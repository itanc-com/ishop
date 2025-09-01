from app.common.exceptions.app_exceptions import DatabaseOperationException
from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartItemRead, CartRead


class ReadCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int) -> CartRead | None:
        try:
            cart_items_dtos = await self.cart_item_repository.find_all_with_products(user_id)
        except Exception as e:
            raise DatabaseOperationException(operation="select", message=str(e), data={"user_id": user_id})

        items_read: list[CartItemRead] = [
            CartItemRead(
                user_id=dto.user_id,
                product_id=dto.product_id,
                quantity=dto.quantity,
                title=dto.title,
                sku=dto.sku,
                price=dto.price_cart,
                total=dto.total,
                date_created_gmt=dto.date_created,
                date_modified_gmt=dto.date_modified,
            )
            for dto in cart_items_dtos
        ]

        if not items_read:
            return None

        cart_read = CartRead(items=items_read)
        return cart_read
