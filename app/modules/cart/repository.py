from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product

from .dtos import CartItemDTO
from .models import CartItem
from .repository_interface import CartRepositoryInterface


class CartRepository(CartRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        self.session.add_all(cart_items)
        await self.session.commit()
        for cart_item in cart_items:
            await self.session.refresh(cart_item)
        return cart_items

    async def insert(self, cart_item: CartItem) -> CartItem:
        self.session.add(cart_item)
        await self.session.commit()
        await self.session.refresh(cart_item)

        # Clone to new object with all database-generated fields
        # to avoid MissingGreenlet errors and detached from session
        inserted_cart_item = CartItem(
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.price,
            subtotal=cart_item.subtotal,
            date_created=cart_item.date_created,
            date_modified=cart_item.date_modified,
        )

        return inserted_cart_item

    async def update(self, updated_cart_item: CartItem) -> CartItem | None:
        db_cart_item = await self.session.get(CartItem, (updated_cart_item.user_id, updated_cart_item.product_id))
        if not db_cart_item:
            return None

        db_cart_item.quantity = updated_cart_item.quantity
        db_cart_item.price = updated_cart_item.price
        db_cart_item.subtotal = updated_cart_item.subtotal

        await self.session.commit()
        await self.session.refresh(db_cart_item)
        return db_cart_item

    async def delete(self, user_id: int, product_id: int) -> None:
        # Directly run a delete query since we don't need to check for cascades or related objects.
        stmt = delete(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def bulk_update(self, cart_items: list[CartItem]) -> None:
        """Bulk update cart items using run_sync for compatibility"""
        if not cart_items:
            return

        mappings = [
            {
                "user_id": item.user_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.subtotal,
                "date_modified": item.date_modified,
            }
            for item in cart_items
        ]

        # Run sync method in async context
        await self.session.run_sync(lambda session: session.bulk_update_mappings(CartItem, mappings))
        await self.session.commit()

    async def bulk_delete_except(self, user_id: int, product_ids_to_keep: list[int]) -> None:
        """
        Delete all cart items for a user except those with product IDs in product_ids_to_keep.
        """
        stmt = delete(CartItem).where(CartItem.user_id == user_id, ~CartItem.product_id.in_(product_ids_to_keep))
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_all(self, user_id: int) -> list[CartItem]:
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_with_products(self, user_id: int) -> list[CartItemDTO]:
        """Get cart items with product details via JOIN, using cart item's stored price."""
        stmt = (
            select(
                CartItem.user_id,
                CartItem.product_id,
                CartItem.quantity,
                CartItem.price,
                CartItem.subtotal,
                CartItem.date_created,
                CartItem.date_modified,
                Product.title,
                Product.sku,
                Product.price.label("price_product"),
                Product.is_available,
            )
            .join(Product, CartItem.product_id == Product.id)
            .where(CartItem.user_id == user_id)
        )

        result = await self.session.execute(stmt)
        rows = result.fetchall()

        return [
            CartItemDTO(
                user_id=row.user_id,
                product_id=row.product_id,
                quantity=row.quantity,
                price_cart=row.price,
                subtotal=row.subtotal,
                date_created=row.date_created,
                date_modified=row.date_modified,
                title=row.title,
                sku=row.sku,
                price_product=row.price_product,
                is_available=row.is_available,
            )
            for row in rows
        ]

    async def get_item(self, user_id: int, product_id: int) -> CartItem | None:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def has_item(self, user_id: int, product_id: int) -> bool:
        """Check if a specific item exists in user's cart."""
        stmt = select(CartItem.user_id).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def delete_all_items(self, user_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def has_cart_items(self, user_id: int) -> bool:
        """Check if user has any items in their cart."""
        stmt = select(CartItem.user_id).where(CartItem.user_id == user_id).limit(1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
