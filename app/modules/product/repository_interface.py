from abc import ABC, abstractmethod
from typing import Any

from .models import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update_by_id(self, product_id: int, updated_product: Product) -> Product:
        pass

    @abstractmethod
    async def delete_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def list_all(self, category_id: int | None = None, skip: int = 0, limit: int = 10) -> list[Product]:
        pass

    @abstractmethod
    async def list_by_ids(self, product_ids: list[int]) -> list[Product]:
        pass

    @abstractmethod
    async def exists_by_field(self, field: str, value: Any) -> bool:
        pass

    @abstractmethod
    async def count_all(self, category_id: int | None = None) -> int:
        pass
