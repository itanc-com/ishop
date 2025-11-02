from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead


class UserDeleteByEmail:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, email: str) -> UserRead:
        get_user = None

        try:
            get_user: User | None = await self.user_repository.get_by_email(email)
        except Exception as e:
            raise DatabaseOperationException(operation="select", message=str(e), data={"email": email})

        if not get_user:
            raise EntityNotFoundException(
                data={"user_id": get_user.id}, message=f"User with ID {get_user.id} not found."
            )

        try:
            user: User | None = await self.user_repository.delete_by_id(get_user.id)
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e), data={"user_id": user.id})

        if not user:
            raise EntityNotFoundException(data={"user_id": user.id}, message=f"User with ID {user.id} not found.")

        return UserRead.model_validate(user)
