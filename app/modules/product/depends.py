from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.product.repository import ProductRepository
from app.modules.product.repository_interface import ProductRepositoryInterface


def get_product_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProductRepositoryInterface:
    return ProductRepository(db_session)
