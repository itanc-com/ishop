from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.category.repository import CategoryRepository
from app.modules.category.repository_interface import CategoryRepositoryInterface


def get_category_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CategoryRepositoryInterface:
    return CategoryRepository(db_session)
