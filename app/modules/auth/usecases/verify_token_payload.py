from app.common.enums import UserRole
from app.common.exceptions.app_exceptions import (
    AuthenticationException,
    InternalServerException,
    NotFoundException,
)
from app.common.http_response.error_response import ErrorCodes
from app.modules.auth.schemas import JWTPayload, TokenType
from app.modules.user.models import User
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
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message=str(e),
                data={"user_id": token_payload.sub},
            )

        user_role = str(UserRole(user.role).name.lower())
        if user is None:
            #! avoid user enumeration
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found", data={"user_id": token_payload.sub}
            )

        if not user_role == token_payload.role:
            #! avoid user enumeration
            raise NotFoundException(
                code=ErrorCodes.ENTITY_NOT_FOUND,
                message="User with this role not found",
                data={"user_id": token_payload.sub},
            )

        if not token_type.value == token_payload.typ:
            #! avoid user enumeration
            raise AuthenticationException(
                code=ErrorCodes.INVALID_CREDENTIALS, message="Invalid credentials", data={"user_id": token_payload.sub}
            )

        expected_payload = dict(typ=token_type.value, role=token_payload.role)

        try:
            result_verification = JWThandler.verify_token(token_payload.model_dump(), expected_payload)
        except ValueError:
            raise AuthenticationException(
                code=ErrorCodes.INVALID_CREDENTIALS,
                message="Invalid credentials",
            )
        if not result_verification:
            raise AuthenticationException(
                code=ErrorCodes.INVALID_CREDENTIALS,
                message="Invalid credentials",
            )
        return UserRead.model_validate(user, from_attributes=True)
