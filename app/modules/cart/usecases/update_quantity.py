from app.common.exceptions.app_exceptions import (
    BadRequestException,
    InternalServerException,
    NotFoundException,
)
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartItemInUpdate, CartItemOutRead


class UpdateCartItemQuantity:
    def __init__(
        self,
        cart_repository: CartRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, user_id: int, cart_item_in_update: CartItemInUpdate) -> CartItemOutRead | None:
        """
        Update the quantity of a cart item.

        - If quantity = 0, remove the item from cart (returns None)
        - If quantity > 0, update the quantity and recalculate total
        - Raises NotFoundException if item not in cart
        - Raises ConflictException if quantity < 0
        """

        if cart_item_in_update.quantity < 0:
            raise BadRequestException(
                code=ErrorCodes.INVALID_REQUEST,
                message="Quantity cannot be negative",
                data={"quantity": cart_item_in_update.quantity},
            )

        # Check if item exists in cart
        exist_cart_item: CartItem | None = await self.cart_repository.get_item(
            user_id=user_id, product_id=cart_item_in_update.product_id
        )

        if not exist_cart_item:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="Item not found in cart",
                data={"user_id": user_id, "product_id": cart_item_in_update.product_id},
            )

        # get the product details for response
        product = await self.product_repository.get_by_id(cart_item_in_update.product_id)
        if not product:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="Product not available anymore",
                data={"product_id": cart_item_in_update.product_id},
            )

        product_title = product.title
        product_sku = product.sku
        product_price = float(product.price)

        # If quantity is 0, remove item from cart
        if cart_item_in_update.quantity == 0:
            try:
                await self.cart_repository.delete(user_id=user_id, product_id=cart_item_in_update.product_id)
                return None

            except Exception as e:
                raise InternalServerException(
                    code=ErrorCodes.DATABASE_ERROR, message="Failed to remove item from cart"
                ) from e

        # if quantity > 0:
        # Update quantity and total
        exist_cart_item.price = product_price
        exist_cart_item.quantity = cart_item_in_update.quantity
        exist_cart_item.subtotal = float(product_price * cart_item_in_update.quantity)

        try:
            updated_cart_item: CartItem = await self.cart_repository.update(exist_cart_item)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to update cart item quantity"
            ) from e

        return CartItemOutRead(
            product_id=updated_cart_item.product_id,
            quantity=updated_cart_item.quantity,
            title=product_title,
            sku=product_sku,
            price=updated_cart_item.price,
            subtotal=updated_cart_item.subtotal,
            date_created_gmt=updated_cart_item.date_created,
            date_modified_gmt=updated_cart_item.date_modified,
        )
