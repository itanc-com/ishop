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
        return cart_item

    async def remove(self, user_id: int, product_id: int) -> None:
        # Directly run a delete query since we don't need to check for cascades or related objects.
        stmt = delete(self.model_class).where(
            self.model_class.user_id == user_id, self.model_class.product_id == product_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_all(self, user_id: int) -> list[CartItem]:
        stmt = select(self.model_class).where(self.model_class.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_with_products(self, user_id: int) -> list[CartItemWithProductDTO]:
        """Get cart items with product details via JOIN, using cart item's stored price."""
        stmt = (
            select(
                self.model_class.user_id,
                self.model_class.product_id,
                self.model_class.quantity,
                self.model_class.price,  # ← Use cart item's price (when added)
                self.model_class.total,
                self.model_class.date_created,
                self.model_class.date_modified,
                Product.title,
                Product.sku,
                Product.price.label("price_product"),  # ← Current product price
            )
            .join(Product, self.model_class.product_id == Product.id)
            .where(self.model_class.user_id == user_id)
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
        stmt = select(self.model_class).where(
            self.model_class.user_id == user_id, self.model_class.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def clear_cart(self, user_id: int) -> None:
        await self.session.execute(CartItem.__table__.delete().where(CartItem.user_id == user_id))
        await self.session.commit()

    async def has_cart_items(self, user_id: int) -> bool:
        """Check if user has any items in their cart."""
        stmt = select(self.model_class.user_id).where(self.model_class.user_id == user_id).limit(1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
