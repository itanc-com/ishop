from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, user: User) -> User:
        
        self.session.add(user)
        await self.session.commit() 
        await self.session.refresh(user)   
        return user

    
    async def email_exists(self, email: str) -> bool:
        query = select(1).where(User.email == email).limit(1)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None   

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    