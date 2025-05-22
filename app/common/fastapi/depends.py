from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.product.repository import ProductRepository
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.user.repository import UserRepository
from app.modules.user.repository_interface import UserRepositoryInterface


def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepositoryInterface:
    return UserRepository(db_session)

def get_product_repository(db_session: AsyncSession = Depends(get_db_session)) -> ProductRepositoryInterface:
    return ProductRepository(db_session)