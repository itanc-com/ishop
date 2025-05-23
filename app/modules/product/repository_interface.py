from abc import ABC, abstractmethod

from .models import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product_id: int, updated_product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def list_all(self, category_id: int | None = None, skip: int = 0, limit: int = 10) -> list[Product]:
        pass

    @abstractmethod
    async def sku_exists(self, sku: str) -> bool:
        pass
