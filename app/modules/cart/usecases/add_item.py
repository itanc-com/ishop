from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..schemas import CartItemCreate, CartItemRead


class AddItemToCart:
    def __init__(
        self, cart_item_repository: CartItemRepositoryInterface, product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_item_create: CartItemCreate) -> CartItemRead | None:
        product_exists = await self.product_repository.get_by_id(cart_item_create.product_id)
        if not product_exists:
            raise EntityNotFoundException(
                data={"product_id": cart_item_create.product_id},
                message=f"Product with id {cart_item_create.product_id} not found",
            )

        existing = await self.cart_item_repository.get_by_user_and_product(
            user_id=cart_item_create.user_id,
            product_id=cart_item_create.product_id,
        )
        if existing:
            raise DuplicateEntryException(
                field="product_id",
                value=str(cart_item_create.product_id),
            )

        cart_item = self.cart_item_repository.model_class(
            user_id=cart_item_create.user_id,
            product_id=cart_item_create.product_id,
            quantity=cart_item_create.quantity,
        )

        try:
            inserted = await self.cart_item_repository.insert(cart_item)
        except Exception as e:
            raise DatabaseOperationException(operation="insert", message=str(e))

        return self._map_to_read(inserted)

    def _map_to_read(self, cart_item) -> CartItemRead:
        """Map CartItem ORM object to CartItemRead schema."""
        return CartItemRead(
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
