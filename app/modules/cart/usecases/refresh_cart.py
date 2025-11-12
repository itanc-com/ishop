from app.common.exceptions.app_exceptions import InternalServerException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.utils.date_time import get_current_utc

from ..dtos import CartItemDTO
from ..models import CartItem
from ..schemas import CartItemOutRead, CartOutRead


class RefreshCart:
    def __init__(
        self, cart_repository: CartRepositoryInterface, product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, user_id: int) -> CartOutRead:
        # fetch current available products which their information in the catalog
        try:
            cart_items_list_db: list[CartItemDTO] = await self.cart_repository.find_all_with_products(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve cart items", data={"user_id": user_id}
            ) from e

        if not cart_items_list_db:
            return CartOutRead(total=0.0, items=[])

        product_ids_to_keep: list[int] = []
        cart_items_update: list[CartItem] = []
        cart_out_read: CartOutRead = CartOutRead(total=0.0, items=[])

        for cart_item in cart_items_list_db:
            if cart_item.is_available:
                product_ids_to_keep.append(cart_item.product_id)

                cart_items_update.append(
                    CartItem(
                        user_id=cart_item.user_id,
                        product_id=cart_item.product_id,
                        quantity=cart_item.quantity,
                        price=cart_item.price_product,
                        subtotal=float(cart_item.price_product) * cart_item.quantity,
                        date_created=cart_item.date_created,
                        date_modified=get_current_utc(),
                    )
                )

                cart_out_read.total += float(cart_item.price_product) * cart_item.quantity
                cart_out_read.items.append(
                    CartItemOutRead(
                        user_id=cart_item.user_id,
                        product_id=cart_item.product_id,
                        title=cart_item.title,
                        sku=cart_item.sku,
                        quantity=cart_item.quantity,
                        price=cart_item.price_product,
                        subtotal=float(cart_item.price_product) * cart_item.quantity,
                        is_available=cart_item.is_available,
                        date_created=cart_item.date_created,
                        date_modified=get_current_utc(),
                    )
                )

        try:
            await self.cart_repository.bulk_delete_except(user_id, product_ids_to_keep)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to delete unavailable cart items",
                data={"user_id": user_id, "product_ids_to_keep": product_ids_to_keep},
            ) from e

        try:
            await self.cart_repository.bulk_update(cart_items_update)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to insert cart items",
                data={"user_id": user_id, "cart_items": cart_items_update},
            ) from e

        return cart_out_read
