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
from app.modules.user.schemas import UserRead

from .depends import get_current_authenticated_user
from .schemas import OAuth2TokenResponse, TokenResponse
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
    # response_model=SuccessResponse[dict],
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


@router.post(
    "/token/swagger",
    response_model=OAuth2TokenResponse,
    include_in_schema=True,
    summary="OAuth2 Token for Swagger UI",
    description="This endpoint is used to obtain an OAuth2 token for Swagger UI.",
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Token retrieved successfully", OAuth2TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_swagger_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
):
    """
    Swagger UI token endpoint.
    This endpoint is used to obtain an OAuth2 token for Swagger UI.
    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        user_repo (UserRepositoryInterface): User repository dependency.
    Returns:
        dict: Access token and token type.
    """
    user = await AuthenticateUserByEmailPassword(user_repo).execute(form_data.username, form_data.password)
    user_role = str(UserRole(user.role).name.lower())

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()

    return {"access_token": tokens.access_token, "token_type": "bearer"}


@router.get(
    "/me",
    description="Get current user information",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User retrieved successfully", UserRead),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_get_me(
    request: Request,
    user: Annotated[UserRead, Depends(get_current_authenticated_user)],
) -> SuccessResponse[UserRead]:
    """
    Get current user information.
    This endpoint retrieves the information of the currently authenticated user.
    Args:
        request (Request): The FastAPI request object.
        user (UserRead): The authenticated user object.
    Returns:
        SuccessResponse[UserRead]: A success response containing the user information.
    """
    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=user,
    )
    return success_response_builder(result, request)


@router.post(
    "/token/refresh",
    description="Refresh tokens using refresh token",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tokens refreshed successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_refresh_tokens(
    request: Request,
    refresh_token: str,
    user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenResponse]:
    """
    Refresh tokens using refresh token.
    This endpoint allows the user to refresh their access and refresh tokens.
    Args:
        request (Request): The FastAPI request object.
        user (UserRead): The authenticated user object.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        SuccessResponse[TokenResponse]: A success response containing the new tokens.
    """
    pass


@router.get(
    "/token/refresh/verify",
    description="Verify refresh token",
    response_model=SuccessResponse[TokenResponse],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Refresh token verified successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_verify_refresh_token(
    request: Request,
    refresh_token: str,
    user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenResponse]:
    """
    Verify refresh token.
    This endpoint allows the user to verify their refresh token.
    Args:
        request (Request): The FastAPI request object.
        user (UserRead): The authenticated user object.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        SuccessResponse[TokenResponse]: A success response containing the verified tokens.
    """
    pass
