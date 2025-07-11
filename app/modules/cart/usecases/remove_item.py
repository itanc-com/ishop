from app.modules.cart.repository_interface import CartItemRepositoryInterface


class RemoveItemFromCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int, product_id: int) -> None:
        """
        This method will remove a specific cart item by given user_id and product_id.
        It will call the repository's remove method to delete the cart item.
        If the item does not exist, it will raise an EntityNotFoundException.
        If the removal fails, it will raise a DatabaseOperationException.
        If the item is successfully removed, it will return None or decide what to return based on the implementation.
        """

        pass
