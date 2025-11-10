from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
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
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve user by email", data={"email": email}
            ) from e

        if not get_user:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="User not found.",
                data={"email": email},
            )

        try:
            user: User | None = await self.user_repository.delete_by_id(get_user.id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to delete user.", data={"user_id": user.id}
            ) from e

        if not user:
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found.", data={"user_id": user.id}
            )

        return UserRead.model_validate(user)
