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
        2. If no items are found, return an empty CartRead (Null Object Pattern).
        3. Map entity models to CartItemRead DTOs.
        4. Return a CartRead object containing all cart items.

        Raises:
           DatabaseOperationException: If retrieving items fails.

        Returns:
           CartRead: Always returns a CartRead object (possibly with an empty items list).
        """

        try:
            cart_items = await self.cart_item_repository.find_all(user_id)
        except Exception as e:
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
