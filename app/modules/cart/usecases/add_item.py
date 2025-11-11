from app.common.exceptions.app_exceptions import (
    InternalServerException,
    NotFoundException,
)
from app.common.http_response.error_response import ErrorCodes
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..repository_interface import CartRepositoryInterface
from ..schemas import CartItemInCreate, CartItemOutRead


class AddItemToCart:
    def __init__(
        self,
        cart_repository: CartRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, cart_item_create: CartItemInCreate, user_id: str) -> CartItemOutRead | None:
        try:
            product: Product | None = await self.product_repository.get_by_id(cart_item_create.product_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="failed to retrieve product information",
                data={"product_id": cart_item_create.product_id},
            ) from e

        if not product:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                data={"product_id": cart_item_create.product_id},
                message="Product not found",
            )

        # Extract product attributes while session is still active
        product_title = product.title
        product_sku = product.sku
        product_price = float(product.price)

        try:
            # get existing cart item to prepare for update if exists
            existing_item: CartItem | None = await self.cart_repository.get_item(
                user_id=user_id,
                product_id=cart_item_create.product_id,
            )

        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="failed to retrieve existing cart item",
                data={"user_id": user_id, "product_id": cart_item_create.product_id},
            ) from e

        if existing_item is None:
            # If not exists, create new
            cart_item = CartItem(
                user_id=user_id,
                **cart_item_create.model_dump(),
                price=product_price,
                subtotal=product_price * cart_item_create.quantity,
            )
            try:
                inserted_item: CartItem = await self.cart_repository.insert(cart_item)
            except Exception as e:
                raise InternalServerException(
                    code=ErrorCodes.DATABASE_ERROR,
                    message="failed to insert new cart item",
                    data={"user_id": user_id, "product_id": cart_item_create.product_id},
                ) from e

            return CartItemOutRead(
                product_id=inserted_item.product_id,
                quantity=inserted_item.quantity,
                title=product_title,
                sku=product_sku,
                price=inserted_item.price,
                subtotal=inserted_item.subtotal,
                date_created_gmt=inserted_item.date_created,
                date_modified_gmt=inserted_item.date_modified,
            )

        # If exists, increase quantity
        if existing_item:
            existing_item.quantity += cart_item_create.quantity
            existing_item.total = existing_item.price * existing_item.quantity
            updated_item = await self.cart_repository.update(existing_item)

        return CartItemOutRead(
            product_id=updated_item.product_id,
            quantity=updated_item.quantity,
            title=product_title,
            sku=product_sku,
            price=updated_item.price,
            total=updated_item.total,
            date_created_gmt=updated_item.date_created,
            date_modified_gmt=updated_item.date_modified,
        )
