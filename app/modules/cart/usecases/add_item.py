from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..schemas import CartItemCreate, CartItemRead
from ..models import CartItem


class AddItemToCart:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
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

        try:
            existing_cart_item = await self.cart_item_repository.get_by_user_and_product(
                user_id=cart_item_create.user_id,
                product_id=cart_item_create.product_id,
            )
        except SQLAlchemyError as e:
            raise DatabaseOperationException(
                operation="read",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        if existing_cart_item:
            raise DuplicateEntryException(field="product_id", value=str(cart_item_create.product_id))

        cart_item: CartItem = self.cart_item_repository.model_class(
            user_id=cart_item_create.user_id,
            product_id=cart_item_create.product_id,
            quantity=cart_item_create.quantity,
        )

        try:
            inserted = await self.cart_item_repository.insert(cart_item)
        except IntegrityError as e:
            await self.cart_item_repository.session.rollback()
            raise DuplicateEntryException(field="product_id", value=str(cart_item_create.product_id))
        except SQLAlchemyError as e:
            await self.cart_item_repository.session.rollback()
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        return CartItemRead(
            user_id=inserted.user_id,
            product_id=inserted.product_id,
            quantity=inserted.quantity,
            title=getattr(inserted, "title", ""),
            sku=getattr(inserted, "sku", ""),
            price=getattr(inserted, "price", 0.0),
            total=getattr(inserted, "total", 0.0),
            date_created_gmt=getattr(inserted, "date_created", None),
            date_modified_gmt=getattr(inserted, "date_modified", None),
        )
