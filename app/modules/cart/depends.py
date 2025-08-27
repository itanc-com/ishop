from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

from .repository import CartItemRepository
from .repository_interface import CartItemRepositoryInterface


def get_cartitem_repository(db_session: AsyncSession = Depends(get_db_session)) -> CartItemRepositoryInterface:
    return CartItemRepository(db_session)
