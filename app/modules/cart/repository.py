from sqlalchemy.ext.asyncio import AsyncSession

from .models import CartItem
from .repository_interface import CartItemRepositoryInterface


class CartItemRepository(CartItemRepositoryInterface):
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