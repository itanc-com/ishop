from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.common.http_response.reponses import ResponseError
from app.db.session import get_session


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
async def login_get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    #user_repo: UserRepo = Depends(get_user_repo),
) -> dict | None:
    """
    Authenticate user and provide access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        dict | None: Access token and refresh token if authentication is successful, None otherwise.
    """
    # user = await user_repo.authenticate(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # return {"access_token": user.access_token, "refresh_token": user.refresh_token}
    pass