from abc import ABC, abstractmethod

from .models import CartItem


class CartItemRepositoryInterface(ABC):
    @abstractmethod
    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        pass

    @abstractmethod
    async def insert(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def update(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def remove(self, product_id: int, user_id: int) -> CartItem:
        pass
