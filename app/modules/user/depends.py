from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

from .repository import UserRepository
from .repository_interface import UserRepositoryInterface


def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> UserRepositoryInterface:
    return UserRepository(db_session)
