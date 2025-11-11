from datetime import datetime, timezone

from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartItemOutRead, CartOutRead


class ReadCart:
    def __init__(
        self, cart_repository: CartRepositoryInterface, product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, user_id: int) -> CartOutRead:
        """
        Sync cart items with current product data

        Algorithm:
        1. Extract product IDs from cart
        2. Fetch products in single query (O(1) DB call)
        3. Create hash map for O(1) lookups
        4. Compare and update cart items
        5. Batch update database

        Rules:
        - If product removed/N/A: Set is_available=False (keep in cart)
        - If price changes: Update price_cart, subtotal, date_modified
        - If title changes: Update title, date_modified

        Returns:
            Tuple of (updated_cart_items, sync_result)
        """

        try:
            cart_items_list_db: list[CartItem] = await self.cart_repository.find_all(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve cart items", data={"user_id": user_id}
            ) from e

        if not cart_items_list_db:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="Cart not found",
                data={"user_id": user_id, "items": []},
            )

        product_ids: list[int] = [item.product_id for item in cart_items_list_db]

        products = await self.product_repository.list_by_ids(product_ids)

        # Create hash map for O(1) lookup
        product_map = {product.id: product for product in products}

        CartItemsOut = []

        for cart_item in cart_items_list_db:
            if cart_item.product_id not in product_map:
                CartItemsOut.append(
                    CartItemOutRead(
                        product_id=cart_item.product_id,
                        quantity=cart_item.quantity,
                        title=cart_item.title,
                        sku=cart_item.sku,
                        price=cart_item.price_cart,
                        subtotal=cart_item.subtotal,
                        is_available=False,
                        date_created_gmt=cart_item.date_created,
                        date_modified_gmt=datetime.now(timezone.utc),
                    )
                )

            else:
                product_info: Product = product_map[cart_item.product_id]

                CartItemsOut.append(
                    CartItemOutRead(
                        product_id=product_info.id,
                        quantity=cart_item.quantity,
                        title=product_info.title,
                        sku=product_info.sku,
                        price=product_info.price,
                        subtotal=float(product_info.price) * cart_item.quantity,
                        is_available=product_info.is_available,
                        date_created_gmt=cart_item.date_created,
                        date_modified_gmt=datetime.now(timezone.utc),
                    )
                )

        return CartOutRead(items=CartItemsOut, total=sum(item.subtotal for item in CartItemsOut))
