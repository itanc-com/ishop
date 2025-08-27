from abc import ABC, abstractmethod
from typing import Any

from .models import CartItem


class CartItemRepositoryInterface(ABC):
    model_class = CartItem

    @abstractmethod
    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        pass

    @abstractmethod
    async def insert(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def remove(self, user_id, product_id):
        pass

    @abstractmethod
    async def find_all(self, user_id: int) -> list[CartItem]:
        pass

    @abstractmethod
    async def clear_cart(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_user_and_product(self, user_id: int, product_id: int) -> Any | None:
        pass
