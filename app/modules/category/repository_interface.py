from abc import ABC, abstractmethod

from app.modules.category.models import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    async def list_all(self, parent_id: int = 0) -> list[Category]:
        pass

    @abstractmethod
    async def delete(self, category: Category) -> None:
        pass
