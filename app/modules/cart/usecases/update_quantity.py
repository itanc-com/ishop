from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartItemRead


class UpdateCartItemQuantity:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int, product_id: int, qty: int) -> CartItemRead | None:
        """
        This method will update the quantity of a specific cart item for a user.
        When the quantity is updated, it calculates the total price based on the new quantity.
        If the item does not exist, it will raise an EntityNotFoundException.
        If the update fails, it will raise a DatabaseOperationException.
        The return value is a CartItemRead object containing the updated cart item details.
        If the cart item does not exist, it will return None.
        If the quantity is set to zero, it will remove the item from the cart.
        If the item is removed, it will return None.
        If the item is updated, it will return the updated CartItemRead object.
        """

        pass
