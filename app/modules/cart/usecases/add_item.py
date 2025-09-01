from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartItemCreate, CartItemRead


class AddItemToCart:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_item_create: CartItemCreate) -> CartItemRead | None:
        product: Product | None = await self.product_repository.get_by_id(cart_item_create.product_id)
        if not product:
            raise EntityNotFoundException(
                data={"product_id": cart_item_create.product_id},
                message=f"Product with id {cart_item_create.product_id} not found",
            )

        try:
            existing_cart_item = await self.cart_item_repository.get_item(
                user_id=cart_item_create.user_id,
                product_id=cart_item_create.product_id,
            )
        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        if existing_cart_item:
            raise DuplicateEntryException(field="product_id", value=str(cart_item_create.product_id))

        cart_item: CartItem = self.cart_item_repository.model_class(
            user_id=cart_item_create.user_id,
            product_id=cart_item_create.product_id,
            quantity=cart_item_create.quantity,
            price=product.price,
            total=product.price * cart_item_create.quantity,
        )

        try:
            inserted = await self.cart_item_repository.insert(cart_item)
        except Exception as e:
            raise DatabaseOperationException(
                operation="insert",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        new_cart_item = CartItemRead(
            user_id=inserted.user_id,
            product_id=inserted.product_id,
            quantity=inserted.quantity,
            title=product.title,
            sku=product.sku,
            price=inserted.price,
            total=inserted.total,
            date_created_gmt=inserted.date_created,
            date_modified_gmt=inserted.date_modified,
        )

        return new_cart_item
