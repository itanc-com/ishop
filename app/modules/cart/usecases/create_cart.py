from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartInCreate, CartItemOutRead, CartOutRead

# * this usecase need to implement after implementing authentication
#! It needs to be carefully reviewed and have very robust tests written for it.


class CartCreateFromBulkItems:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_in_create: CartInCreate, user_id: str) -> CartOutRead | None:
        if not cart_in_create.items:
            return None

        #! This UseCase need to implement after implementing authentication
        # TODO check that the username of the user obtained from get_current_authenticated_user
        # TODO the user mustmatches the one in cart_in_create otherwise raise exception

        # ? get current_user
        # temporary user_id assigned by path parameter and assumed its authenticated user id

        # Verify all items are for the same user (business rule)
        user_ids = {item.user_id for item in cart_in_create.items}
        if len(user_ids) > 1:
            raise DatabaseOperationException(
                operation="validation",
                message="All items in a bulk create request must belong to the same user.",
                data={"user_ids": list(user_ids)},
            )

        unique_user_id = next(iter(user_ids))  # Get the single user_id

        # TODO check unique_user_id matches user_id from parameter or get_current_authenticated_user

        # Check if user already has items in cart (new business rule)
        try:
            has_existing_items = await self.cart_item_repository.has_cart_items(user_id)
        except Exception as e:
            raise DatabaseOperationException(operation="read", message=str(e), data={"user_id": user_id})

        if has_existing_items:
            raise DuplicateEntryException(
                field="cart", value=f"User {unique_user_id} already has items in cart. Clear cart before bulk insert."
            )

        # Validate all products exist and prepare cart items with pricing
        cart_items: list[CartItem] = []

        for item in cart_in_create.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise EntityNotFoundException(
                    data={"product_id": item.product_id, "cart": cart_items},
                    message=f"Product with id {item.product_id} not found, Cannot create cart.",
                )

            cart_item = self.cart_item_repository.model_class(
                user_id=item.user_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price,
                total=product.price * item.quantity,
            )
            cart_items.append(cart_item)

        # Insert all cart items in bulk
        try:
            inserted_items: list[CartItem] = await self.cart_item_repository.bulk_insert(cart_items)
        except Exception as e:
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={
                    "items": [
                        {"user_id": cart_item.user_id, "product_id": cart_item.product_id} for cart_item in cart_items
                    ]
                },
            )

        items_read: list[CartItemOutRead] = [
            CartItemOutRead(
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
            for cart_item in inserted_items
        ]

        return CartOutRead(items=items_read)
