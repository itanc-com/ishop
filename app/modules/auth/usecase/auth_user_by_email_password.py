from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    EntityNotFoundException,
    InvalidCredentialsException,
)
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead
from app.utils.security.password_context import PasswordContext


class AuthenticateUserByEmailPassword:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, email: str, raw_password: str) -> UserRead:
        
        try:
            user = await self.user_repository.get_by_email(email)
        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
            )
        
        if not user:
            raise EntityNotFoundException(
                message="User not found",
                data={"email": email},
            )

        if not user or not PasswordContext.verify_password(raw_password, user.password):
            raise InvalidCredentialsException(
                data={"email": email},
                message="Invalid credentials",
            )

        return UserRead.model_validate(user, from_attributes=True)
