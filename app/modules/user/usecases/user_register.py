from app.common.exceptions.app_exceptions import DatabaseOperationException, DuplicateEntryException
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.utils.security.password_context import PasswordContext

from ..schemas import UserCreate, UserRead


class UserRegister:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self,user_create: UserCreate) -> UserRead | None:
        
        if await self.user_repository.email_exists(user_create.email):
            raise DuplicateEntryException("email", user_create.email)
        
        user_data = User(**user_create.model_dump())
        user_data.password = PasswordContext.hash_password(user_create.password)
        
        
        try:
            new_user = await self.user_repository.insert(user_data)
        except Exception as e:
            raise DatabaseOperationException("insert", str(e), data={"user": user_data})
        
        user_read = UserRead.model_validate(new_user)
        
        return user_read
        

      