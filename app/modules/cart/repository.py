from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product

from .dtos import CartItemWithProductDTO
from .models import CartItem
from .repository_interface import CartItemRepositoryInterface


class CartItemRepository(CartItemRepositoryInterface):
    model_class = CartItem

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
            total=cart_item.total,
            date_created=cart_item.date_created,
            date_modified=cart_item.date_modified,
        )

        return inserted_cart_item

    async def remove(self, user_id: int, product_id: int) -> None:
        # Directly run a delete query since we don't need to check for cascades or related objects.
        stmt = delete(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_all(self, user_id: int) -> list[CartItem]:
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_with_products(self, user_id: int) -> list[CartItemWithProductDTO]:
        """Get cart items with product details via JOIN, using cart item's stored price."""
        stmt = (
            select(
                CartItem.user_id,
                CartItem.product_id,
                CartItem.quantity,
                CartItem.price,  # ← Use cart item's price (when added)
                CartItem.total,
                CartItem.date_created,
                CartItem.date_modified,
                Product.title,
                Product.sku,
                Product.price.label("price_product"),  # ← Current product price
            )
            .join(Product, CartItem.product_id == Product.id)
            .where(CartItem.user_id == user_id)
        )

        result = await self.session.execute(stmt)
        rows = result.fetchall()

        return [
            CartItemWithProductDTO(
                user_id=row.user_id,
                product_id=row.product_id,
                quantity=row.quantity,
                price_cart=row.price,
                total=row.total,
                date_created=row.date_created,
                date_modified=row.date_modified,
                title=row.title,
                sku=row.sku,
                price_product=row.price_product,
            )
            for row in rows
        ]

    async def get_item(self, user_id: int, product_id: int) -> CartItem | None:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def has_item(self, user_id: int, product_id: int) -> bool:
        """Check if a specific item exists in user's cart."""
        stmt = select(CartItem.user_id).where(CartItem.user_id == user_id, CartItem.product_id == product_id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def clear_cart(self, user_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def has_cart_items(self, user_id: int) -> bool:
        """Check if user has any items in their cart."""
        stmt = select(CartItem.user_id).where(CartItem.user_id == user_id).limit(1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

