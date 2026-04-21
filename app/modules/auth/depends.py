from fastapi.params import Depends

from app.common.enums import UserRole
from app.common.exceptions import ForbiddenAccessException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.auth.schemas import JWTPayload
from app.modules.auth.usecases.read_jwt_token import ReadJwtToken
from app.modules.user.depends import get_user_repository
from app.modules.user.models import User
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead
from app.utils.security.oauth2_bearer import oauth2_bearer


async def get_current_authenticated_user(
    token: str = Depends(oauth2_bearer),
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
) -> UserRead:
    """
    Get the current authenticated user based on the provided token.

    Args:
        token (str): The access token.
        user_repository (UserRepositoryInterface): The user repository.

    Returns:
        UserRead: The authenticated user.
    """

    payload: JWTPayload = await ReadJwtToken(token).execute()
    user_id = payload.sub
    user: User | None = await user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundException(code=ErrorCodes.ENTITY_NOT_FOUND, message="User not found", data={"user_id": user_id})

    return UserRead.model_validate(user)


async def get_current_user_id(
    current_user: UserRead = Depends(get_current_authenticated_user),
) -> int:
    """
    Get the current authenticated user's ID.

    Args:
        current_user (UserRead): The authenticated user from get_current_authenticated_user.

    Returns:
        int: The user's ID.
    """
    return current_user.id


def role_required(roles: list[UserRole]):
    """
    Create a dependency that restricts access to users with specific roles.

    This is a dependency factory that returns a FastAPI dependency function
    for role-based access control. It authenticates the user and verifies
    they have one of the required roles.

    Args:
        roles (list[UserRole]): List of roles allowed to access the endpoint.

    Returns:
        Callable: A FastAPI dependency function that returns the authenticated UserRead.

    Raises:
        ForbiddenAccessException: If the user's role is not in the allowed roles list.
        AuthenticationException: If the token is invalid or expired.
        NotFoundException: If the user no longer exists in the database.
    """

    def _check_role(user: UserRead = Depends(get_current_authenticated_user)):
        if user.role not in roles:
            raise ForbiddenAccessException(
                code=ErrorCodes.FORBIDDEN,
                message=f"Access denied for {user.role}",
                data={"required_roles": roles, "user_role": user.role},
            )
        return user

    return _check_role
