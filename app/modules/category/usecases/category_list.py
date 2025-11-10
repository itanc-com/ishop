from app.modules.category.schemas import CategoryRead

from ..models import Category
from ..repository_interface import CategoryRepositoryInterface


class CategoryList:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    async def execute(self, parent_id: int = 0) -> list[CategoryRead]:
        categories: list[Category] = await self.category_repository.list_all(parent_id)
        return [CategoryRead.model_validate(category) for category in categories]
