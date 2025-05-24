from fastapi.params import Depends

from app.common.exceptions.app_exceptions import EntityNotFoundException
from app.common.fastapi.depends import get_user_repository
from app.modules.auth.schemas import JWTPayload
from app.modules.auth.usecases.read_access_token import ReadAccessToken
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
    payload: JWTPayload = await ReadAccessToken(token).execute()
    user_id = payload.sub
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise EntityNotFoundException(data={"user_id": user_id}, message="User not found")
    return UserRead.model_validate(user)
