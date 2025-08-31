from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import CartItem
from .repository_interface import CartItemRepositoryInterface


class CartItemRepository(CartItemRepositoryInterface):
    model_class = CartItem

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, cart_item: CartItem) -> CartItem:
        self.session.add(cart_item)
        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_item

    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        self.session.add_all(cart_items)
        await self.session.commit()
        for cart_item in cart_items:
            await self.session.refresh(cart_item)
        return cart_items

    async def find_all(self, user_id: int) -> list[CartItem]:
        stmt = select(self.model_class).where(self.model_class.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def clear_cart(self, user_id: int) -> None:
        await self.session.execute(CartItem.__table__.delete().where(CartItem.user_id == user_id))
        await self.session.commit()

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> CartItem | None:
        stmt = select(self.model_class).where(
            self.model_class.user_id == user_id, self.model_class.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def remove(self, user_id: int, product_id: int) -> None:
        stmt = select(self.model_class).where(
            self.model_class.user_id == user_id, self.model_class.product_id == product_id
        )
        result = await self.session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item:
            await self.session.delete(cart_item)
            await self.session.commit()
