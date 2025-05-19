from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.common.fastapi.depends import get_user_repository
from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult, success_response_builder
from app.modules.user.models import UserRole
from app.modules.user.repository_interface import UserRepositoryInterface

from .schemas import TokenResponse
from .usecases.auth_user_by_email_password import AuthenticateUserByEmailPassword
from .usecases.create_tokens import CreateTokens

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[],
    responses=ResponseErrorDoc.HTTP_404_NOT_FOUND("NOT FOUND"),
)


@router.post(
    "/token",
    description="user authentication and provides access token and refresh token",
    #response_model=SuccessResponse[dict],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Token created successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenResponse]:
    """
    Authenticate user and provide access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        dict | None: Access token and refresh token if authentication is successful, None otherwise.
    """

    email = form_data.username
    password = form_data.password

    user = await AuthenticateUserByEmailPassword(user_repository).execute(email, password)
    
    user_role = str(UserRole(user.role).name.lower())

    create_tokens = CreateTokens(user_id=str(user.id), user_role=user_role)
    tokens = await create_tokens.execute()
    
    result = SuccessResult[TokenResponse](
                code=SuccessCodes.CREATED,
                message="Tokens created successfully",
                status_code=status.HTTP_201_CREATED,
                data=tokens,
            )
        
    return success_response_builder(result, request)
