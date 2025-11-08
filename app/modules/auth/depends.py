from fastapi.params import Depends

from app.common.enums import UserRole
from app.common.exceptions import EntityNotFoundException, ForbiddenAccessException
from app.modules.auth.schemas import JWTPayload
from app.modules.auth.usecases.read_jwt_token import ReadJwtToken
from app.modules.user.depends import get_user_repository
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
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise EntityNotFoundException(data={"user_id": user_id}, message="User not found")
    return UserRead.model_validate(user)


def role_required(roles: list[UserRole]):
    def _check_role(user: UserRead = Depends(get_current_authenticated_user)):
        if user.role not in roles:
            raise ForbiddenAccessException(
                message=f"Access denied for {user.role}", data={"required_roles": roles, "user_role": user.role}
            )
        return user

    return _check_role
