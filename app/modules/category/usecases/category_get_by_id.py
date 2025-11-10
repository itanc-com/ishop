from app.common.exceptions.app_exceptions import NotFoundException
from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.schemas import CategoryRead


class CategoryGetById:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    async def execute(self, category_id: int) -> CategoryRead:
        category = await self.category_repository.get_by_id(category_id)
        if category is None:
            raise NotFoundException(
                data={"category_id": category_id},
                message="Category not found",
            )
        return CategoryRead.model_validate(category)
