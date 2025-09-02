from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.category.models import Category
from app.modules.category.repository_interface import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_by_id(self, category_id: int) -> Category | None:
        query = select(Category).where(Category.id == category_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_all(self, parent_id: int = 0) -> list[Category]:
        query = select(Category).where(Category.parent_id == parent_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.commit()
