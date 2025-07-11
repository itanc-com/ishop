from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartItemCreate, CartItemRead


class AddItemToCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, cart_item_create: CartItemCreate) -> CartItemRead | None:
        """
        This method will Add a new item to the cart.
        It will insert a new cart item to the database using the repository's insert method.
        If the item already exists for the user, it will raise a DuplicateEntryException.
        If the insertion fails, it will raise a DatabaseOperationException.
        The return value is a CartItemRead object containing the details of the added cart item.
        If the cart item is successfully added, it will return the CartItemRead object.
        If the cart item is not added, it will return None.
        If the item is added, it will return the CartItemRead object.
        """

        pass
