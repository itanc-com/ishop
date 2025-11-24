from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

from .repository import CartRepository
from .repository_interface import CartRepositoryInterface


def get_cart_repository(db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> CartRepositoryInterface:
    return CartRepository(db_session)
