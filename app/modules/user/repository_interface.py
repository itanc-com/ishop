from abc import ABC, abstractmethod

from .models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def insert(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass
