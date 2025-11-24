from app.common.exceptions.app_exceptions import (
    AuthenticationException,
    InternalServerException,
)
from app.common.http_response.error_response import ErrorCodes
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead
from app.utils.security.password_context import PasswordContext


class AuthenticateUserByEmailPassword:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, email: str, raw_password: str) -> UserRead:
        try:
            user: User = await self.user_repository.get_by_email(email)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message=str(e),
                data={"email": email},
            )

        # This is a critical security best practice to avoid user enumeration
        # by providing the same error message for both non-existent users and incorrect passwords.

        if not user:
            raise AuthenticationException(
                code=ErrorCodes.INVALID_CREDENTIALS,
                message="Invalid credentials",
                data={"email": email},
            )

        if not PasswordContext.verify_password(raw_password, user.password):
            raise AuthenticationException(
                code=ErrorCodes.INVALID_CREDENTIALS,
                message="Invalid credentials",
                data={"email": email},
            )

        return UserRead.model_validate(user, from_attributes=True)
