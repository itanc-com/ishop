from app.common.exceptions.app_exceptions import (
    BadRequestException,
    ConflictException,
    InternalServerException,
    NotFoundException,
)
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..lib.helpers import merge_cart_items
from ..models import CartItem
from ..schemas import CartInCreate, CartItemOutRead, CartOutRead


class CartCreateFromBulkItems:
    def __init__(
        self,
        cart_repository: CartRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, cart_in_create: CartInCreate, user_id: int) -> CartOutRead | None:
        if not cart_in_create.items:
            raise BadRequestException(
                code=ErrorCodes.INVALID_REQUEST, message="Cannot create cart with empty items list", data={"items": []}
            )

        # Check if user already has items in cart (new business rule)
        try:
            has_existing_items = await self.cart_repository.has_cart_items(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to check user's existing cart",
                data={"user_id": user_id},
            ) from e

        if has_existing_items:
            raise ConflictException(
                code=ErrorCodes.CONFLICT,
                message="Cart already exists. Clear cart before bulk insert",
                data={"user_id": user_id, "items": cart_in_create.items},
            )
        # Merge duplicate product entries by summing their quantities
        merged_items = merge_cart_items(item.model_dump() for item in cart_in_create.items)

        # Validate all products exist and prepare cart items with pricing
        cart_items: list[CartItem] = []

        for item_dict in merged_items:
            product = await self.product_repository.get_by_id(item_dict["product_id"])
            if not product:
                raise NotFoundException(
                    code=ErrorCodes.ENTITY_NOT_FOUND,
                    data={"product_id": item_dict["product_id"]},
                    message="Product not found. Please verify all product IDs are valid.",
                )

            cart_item = CartItem(
                user_id=user_id,
                product_id=item_dict["product_id"],
                quantity=item_dict["quantity"],
                price=float(product.price),
                subtotal=float(product.price * item_dict["quantity"]),
            )

            cart_items.append(cart_item)

        # Insert all cart items in bulk
        try:
            inserted_items: list[CartItem] = await self.cart_repository.bulk_insert(cart_items)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to create cart items in bulk",
                data={
                    "user_id": user_id,
                    "items": [
                        {"product_id": cart_item.product_id, "quantity": cart_item.quantity} for cart_item in cart_items
                    ],
                },
            ) from e

        items_read: list[CartItemOutRead] = [
            CartItemOutRead(
                user_id=cart_item.user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                title=getattr(cart_item, "title", ""),
                sku=getattr(cart_item, "sku", ""),
                price=getattr(cart_item, "price", 0.0),
                subtotal=getattr(cart_item, "subtotal", 0.0),
                date_created_gmt=getattr(cart_item, "date_created", None),
                date_modified_gmt=getattr(cart_item, "date_modified", None),
            )
            for cart_item in inserted_items
        ]

        return CartOutRead(items=items_read)
