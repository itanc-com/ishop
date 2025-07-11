from app.common.exceptions.app_exceptions import DatabaseOperationException, DuplicateEntryException
from app.modules.cart.models import CartItem
from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartBulkCreate, CartRead


class CreateCartFromItems:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self,cart_bulk: CartBulkCreate) -> CartRead | None:
        
        """
        Create a cart from a list of items.
        This method will insert multiple cart items to the database with repository bulk_insert method.
        If any item already exists for the user, it will raise a DuplicateEntryException.
        If the insertion fails, it will raise a DatabaseOperationException.
        The return value is a CartRead object containing the list of CartItemRead objects.
        If the cart is empty, it will return None.
        """
        
        pass
        

      