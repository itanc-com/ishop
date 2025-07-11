from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartRead


class ReadCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int) -> CartRead | None:
        """
        This method will read the cart for a specific user.
        It will retrieve all cart items for the given user_id from the database using the repository's
        find_all method.
        If the user does not have any items in the cart, it will return None.
        If the retrieval fails, it will raise a DatabaseOperationException.
        The return value is a CartRead object containing the list of CartItemRead objects.
        If the cart is empty, it will return None.
        If the cart is successfully retrieved, it will return the CartRead object.
        """

        pass
