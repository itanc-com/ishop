from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
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
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve user by email", data={"email": email}
            ) from e

        if not user:
            raise NotFoundException(code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found.", data={"email": email})

        return UserRead.model_validate(user)
