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
        
        
        #print(f"user_data: {user_data.__dict__}")
        
        # user_data = {
        #     "id": 43,
        #     "first_name": "mike",
        #     "last_name": "toske",
        #     "email": "johnxcxcdxdsds@example.com",
        #     "picture": "https://example.com/photos/123.jpg",
        #     "role": 0,
        #     "status": 0,
        #     "phone": "+15555550123",
        #     "address": "123 Main St, City",
        #     "country": "united states",
        #     "password": "nnuuhuhihihui",
        #     "date_created": "2024-05-18T14:00:00Z",
        #     "date_modified": "2024-05-18T14:00:00Z"
        #     }
        
        try:
            new_user = await self.user_repository.insert(user_data)
        except Exception as e:
            raise DatabaseOperationException("insert", str(e), data={"user": new_user})
        
        user_read = UserRead.model_validate(user_data)
        
        return user_read
        

      