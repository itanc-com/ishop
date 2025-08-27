from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.cart.repository_interface import CartItemRepositoryInterface


class RemoveItemFromCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int, product_id: int) -> None:
        """
        Remove a specific cart item for a given user_id and product_id.
        Raises:
            EntityNotFoundException: if the cart item does not exist.
            DatabaseOperationException: if the deletion fails.
        """

        item = await self.cart_item_repository.get_by_user_and_product(user_id, product_id)
        if not item:
            raise EntityNotFoundException(data={"user_id": user_id, "product_id": product_id})

        try:
            await self.cart_item_repository.remove(user_id=user_id, product_id=product_id)
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e))

        return None
