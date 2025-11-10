from app.common.exceptions.app_exceptions import NotFoundException
from app.common.http_response.error_response import ErrorCodes

from ..models import Category
from ..repository_interface import CategoryRepositoryInterface
from ..schemas import CategoryRead


class CategoryGetById:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    async def execute(self, category_id: int) -> CategoryRead:
        category: Category | None = await self.category_repository.get_by_id(category_id)
        if category is None:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="Category not found",
                data={"category_id": category_id},
            )
        return CategoryRead.model_validate(category)
