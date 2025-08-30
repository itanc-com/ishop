from sqlalchemy import select, tuple_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..schemas import CartBulkCreate, CartItemRead, CartRead
from ..models import CartItem


class CreateCartFromItems:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_bulk: CartBulkCreate) -> CartRead | None:
        if not cart_bulk.items:
            return None

        for item in cart_bulk.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise EntityNotFoundException(
                    data={"product_id": item.product_id},
                    message=f"Product with id {item.product_id} not found",
                )

        user_product: list[tuple[int, int]] = [(item.user_id, item.product_id) for item in cart_bulk.items]
        existing_items_stmt = select(
            self.cart_item_repository.model_class.user_id,
            self.cart_item_repository.model_class.product_id,
        ).where(
            tuple_(
                self.cart_item_repository.model_class.user_id,
                self.cart_item_repository.model_class.product_id,
            ).in_(user_product)
        )

        try:
            existing_items_result = await self.cart_item_repository.session.execute(existing_items_stmt)
        except SQLAlchemyError as e:
            raise DatabaseOperationException(operation="read", message=str(e), data={"pairs": user_product})

        duplicate_entries = set(existing_items_result.fetchall())
        if duplicate_entries:
            duplicates_str = ", ".join([f"(user_id={uid}, product_id={pid})" for uid, pid in duplicate_entries])
            raise DuplicateEntryException(field="user_id_product_id", value=duplicates_str)

        cart_items: list[CartItem] = [
            self.cart_item_repository.model_class(
                user_id=item.user_id, product_id=item.product_id, quantity=item.quantity
            )
            for item in cart_bulk.items
        ]

        try:
            inserted_items: list[CartItem] = await self.cart_item_repository.bulk_insert(cart_items)
        except IntegrityError as e:
            await self.cart_item_repository.session.rollback()
            raise DuplicateEntryException(field="user_id_product_id", value=str(e.orig))
        except SQLAlchemyError as e:
            await self.cart_item_repository.session.rollback()
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={
                    "items": [
                        {"user_id": cart_item.user_id, "product_id": cart_item.product_id}
                        for cart_item in cart_items
                    ]
                },
            )

        items_read: list[CartItemRead] = [
            CartItemRead(
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

        return CartRead(items=items_read)
