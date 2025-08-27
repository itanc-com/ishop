from typing import List

from app.common.exceptions.app_exceptions import DatabaseOperationException
from app.modules.cart.repository_interface import CartItemRepositoryInterface

from ..schemas import CartItemRead, CartRead


class ReadCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int) -> CartRead | None:
        """
        Retrieve the cart items for a specific user.

        Steps:
        1. Query all cart items for the given user_id using the repository.
        2. If no items are found, return None.
        3. Map entity models to CartItemRead DTOs.
        4. Return a CartRead object containing all cart items.

        Raises:
            DatabaseOperationException: If retrieving items fails.

        Returns:
            CartRead | None: Returns None if the user has no cart items.
        """

        try:
            cart_items = await self.cart_item_repository.find_all(user_id)
        except Exception as e:
            raise DatabaseOperationException(operation="find_all", message=str(e), data={"user_id": user_id})

        if not cart_items:
            return None

        items_read: List[CartItemRead] = [
            CartItemRead(
                user_id=ci.user_id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                title=getattr(ci, "title", ""),
                sku=getattr(ci, "sku", ""),
                price=getattr(ci, "price", 0.0),
                total=getattr(ci, "total", 0.0),
                date_created_gmt=getattr(ci, "date_created", None),
                date_modified_gmt=getattr(ci, "date_modified", None),
            )
            for ci in cart_items
        ]

        return CartRead(items=items_read)
