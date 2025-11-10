from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead


class UserGetById:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> UserRead:
        try:
            user: User = await self.user_repository.get_by_id(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve user by ID", data={"user_id": user_id}
            ) from e

        if not user:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found.", data={"user_id": user_id}
            )

        return UserRead.model_validate(user)
