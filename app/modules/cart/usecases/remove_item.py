from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.cart.repository_interface import CartItemRepositoryInterface


class RemoveItemFromCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int, product_id: int) -> None:
        try:
            item = await self.cart_item_repository.get_item(user_id, product_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
                data={"user_id": user_id, "product_id": product_id},
            )

        if not item:
            raise EntityNotFoundException(
                data={"user_id": user_id, "product_id": product_id},
                message=f"Item {product_id} for user with Id {user_id} is not found",
            )

        try:
            await self.cart_item_repository.remove(user_id=user_id, product_id=product_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="delete",
                message=str(e),
                data={"user_id": user_id, "product_id": product_id},
            )
