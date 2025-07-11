from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    EntityNotFoundException,
    InvalidCredentialsException,
)
from app.modules.auth.schemas import JWTPayload, TokenType
from app.modules.user.models import User, UserRole
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead
from app.utils.jwt_auth.jwt_handler import JWThandler


class VerifyTokenPayload:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, token_payload: JWTPayload, token_type: TokenType) -> UserRead:
        try:
            user: User = await self.user_repository.get_by_id(token_payload.sub)
        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
            )

        user_role = str(UserRole(user.role).name.lower())
        if user is None:
            raise EntityNotFoundException(message="User not found")

        if not user_role == token_payload.role:
            raise EntityNotFoundException("User with this role not found")

        if not token_type.value == token_payload.typ:
            raise InvalidCredentialsException(
                message="Invalid credentials",
            )

        expected_payload = dict(typ=token_type.value, role=token_payload.role)

        try:
            result_verification = JWThandler.verify_token(token_payload.model_dump(), expected_payload)
        except ValueError:
            raise InvalidCredentialsException(
                message="Invalid credentials",
            )
        if not result_verification:
            raise InvalidCredentialsException(
                message="Invalid credentials",
            )
        return UserRead.model_validate(user, from_attributes=True)
