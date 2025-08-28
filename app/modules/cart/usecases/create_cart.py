from sqlalchemy import select, tuple_
from sqlalchemy.exc import SQLAlchemyError

from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..schemas import CartBulkCreate, CartItemRead, CartRead


class CreateCartFromItems:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_bulk: CartBulkCreate) -> CartRead | None:
        """
        Create a cart from a list of items.

        Steps:
        1. Validate that cart_bulk is not empty.
        2. Check for duplicate items (user_id + product_id) in a single query.
        3. Map input DTOs to repository models.
        4. Bulk insert into the database with exception handling.
        5. Map inserted items to CartItemRead DTOs.
        6. Return a CartRead containing all items.

        Raises:
            DuplicateEntryException: if any item already exists for the user.
            DatabaseOperationException: if bulk insert fails.

        Returns:
            CartRead | None: Returns None if cart is empty.
        """

        if not cart_bulk.items:
            return None

        for item in cart_bulk.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise EntityNotFoundException(
                    data={"product_id": item.product_id}, message=f"Product with id {item.product_id} not found"
                )

        # Prepare list of (user_id, product_id) tuples
        user_product_pairs: list[tuple[int, int]] = [(item.user_id, item.product_id) for item in cart_bulk.items]

        # Query existing items in one go
        stmt = select(
            self.cart_item_repository.model_class.user_id, self.cart_item_repository.model_class.product_id
        ).where(
            tuple_(self.cart_item_repository.model_class.user_id, self.cart_item_repository.model_class.product_id).in_(
                user_product_pairs
            )
        )

        result = await self.cart_item_repository.session.execute(stmt)
        existing_pairs = set(result.fetchall())

        if existing_pairs:
            duplicates = [{"user_id": uid, "product_id": pid} for uid, pid in existing_pairs]
            raise DuplicateEntryException(field="product_id", value=str([d["product_id"] for d in duplicates]))

        cart_items = [
            self.cart_item_repository.model_class(
                user_id=item.user_id, product_id=item.product_id, quantity=item.quantity
            )
            for item in cart_bulk.items
        ]

        try:
            async with self.session.begin():
                inserted_items = await self.cart_item_repository.bulk_insert(cart_items)
        except SQLAlchemyError as e:
            raise DatabaseOperationException(operation="bulk_insert", message=str(e))

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
