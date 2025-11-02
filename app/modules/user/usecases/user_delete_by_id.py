from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead


class UserDeleteById:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> UserRead:
        user = None

        try:
            user: User | None = await self.user_repository.delete_by_id(user_id)
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e), data={"user_id": user_id})

        if not user:
            raise EntityNotFoundException(data={"user_id": user_id}, message=f"User with ID {user_id} not found.")

        return UserRead.model_validate(user)
