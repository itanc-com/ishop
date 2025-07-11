from app.common.exceptions.app_exceptions import DatabaseOperationException
from app.modules.category.models import Category
from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.schemas import CategoryCreate, CategoryRead


class CategoryCreateUsecase:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    async def execute(self, category_create: CategoryCreate) -> CategoryRead | None:
        category = Category(**category_create.model_dump())
        try:
            category = await self.category_repository.create(category)
        except Exception as e:
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={"category_create": category_create.model_dump()},
            )
        return CategoryRead.model_validate(category)
