from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.schemas import CategoryRead


class CategoryList:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    async def execute(self, parent_id: int = 0) -> list[CategoryRead]:
        categories = await self.category_repository.list_all(parent_id)
        return [CategoryRead.model_validate(category) for category in categories]
