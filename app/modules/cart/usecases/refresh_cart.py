from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..dtos import CartItemDTO
from ..schemas import CartOutRead


class RefreshCart:
    def __init__(
        self, cart_repository: CartRepositoryInterface, product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, user_id: int) -> CartOutRead:
        # fetch current cart items with current product prices
        try:
            cart_items_db_list: list[CartItemDTO] = await self.cart_repository.find_all_with_products(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve cart items", data={"user_id": user_id}
            ) from e

        if not cart_items_db_list:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="Cart not found",
                data={"user_id": user_id, "items": []},
            )

        # cart_bulk_update_list: list[CartItem] = []

        # Compare CartItemDTO title & price with current product price and update if different
        for cart_item_db in cart_items_db_list:
            current_product = await self.product_repository.get_by_id(cart_item_db.product_id)

            if not current_product:
                cart_item_db.is_available = False
                continue
            elif not current_product.is_available:
                cart_item_db.is_available = False
                continue

            if (current_product.price != cart_item_db.price_cart) or (current_product.title != cart_item_db.title):
                cart_item_db.is_available = True
                cart_item_db.title = current_product.title
                cart_item_db.price_cart = current_product.price
                cart_item_db.subtotal = cart_item_db.price_cart * cart_item_db.quantity

            # cart_items_bulk_update_list.append(cart_item_db)

        # await self.cart_repository.bulk_update(cart_items_bulk_update_list)

        #     for cart_item_db in cart_items_db_list:
        #         print(cart_item_db.__dict__)

        # items_read: list[CartItemOutRead] = [
        #     CartItemOutRead(
        #         product_id=item.product_id,
        #         quantity=item.quantity,
        #         title=item.title,
        #         sku=item.sku,
        #         price=item.price_cart,
        #         subtotal=item.subtotal,
        #         date_created_gmt=item.date_created,
        #         date_modified_gmt=item.date_modified,
        #     )
        #     for item in cart_items_dto_list
        # ]

        # return CartOutRead(items=items_read, total=sum(item.subtotal for item in items_read))
        # Bulk update all modified cart items

        return None
