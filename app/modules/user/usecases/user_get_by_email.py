from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead


class UserGetByEmail:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, email: str) -> UserRead:
        try:
            user: User = await self.user_repository.get_by_email(email)
        except Exception as e:
            raise DatabaseOperationException(operation="select", message=str(e), data={"email": email})

        if not user:
            raise EntityNotFoundException(data={"email": email}, message=f"User with email {email} not found")

        return UserRead.model_validate(user)
