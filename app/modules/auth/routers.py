from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.common.http_response.reponses import ResponseError
from app.db.session import get_session
from app.modules.user.models import UserRole
from app.modules.user.repository import UserRepository

from .usecase.auth_user_by_email_password import AuthenticateUserByEmailPassword
from .usecase.create_tokens import CreateTokens

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[],
    responses=ResponseError.HTTP_404_NOT_FOUND("NOT FOUND"),
)


@router.post(
    "/token",
    description="user authentication and provides access token and refresh token",
    response_model=dict | None,
    responses={
        **ResponseError.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseError.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseError.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseError.HTTP_401_UNAUTHORIZED("UNAUTHORIZED"),
    },
)
async def auth_get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]
) -> dict | None:
    """
    Authenticate user and provide access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        dict | None: Access token and refresh token if authentication is successful, None otherwise.
    """

    email = form_data.username
    password = form_data.password

    user = await AuthenticateUserByEmailPassword(session).execute(email, password)
    
    user_role = str(UserRole(user.role).name.lower())

    create_tokens = CreateTokens(user_id=str(user.id), user_role=user_role)
    tokens = await create_tokens.execute()
    return tokens
