from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.common.enums import UserRole
from app.common.http_response.doc_responses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.user.depends import get_user_repository
from app.modules.user.repository_interface import UserRepositoryInterface
from app.modules.user.schemas import UserRead

from .depends import get_current_authenticated_user
from .schemas import JWTPayload, OAuth2TokenResponse, TokenResponse, TokenType, UserLoginRequest
from .usecases.auth_user_by_email_password import AuthenticateUserByEmailPassword
from .usecases.create_tokens import CreateTokens
from .usecases.read_jwt_token import ReadJwtToken
from .usecases.verify_token_payload import VerifyTokenPayload

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[],
    responses=ResponseErrorDoc.HTTP_404_NOT_FOUND("NOT FOUND"),
)


@router.post(
    "/token",
    description="user authentication and provides access token and refresh token",
    response_model=SuccessResponse[TokenResponse],
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
    request: Request,
    credentials: UserLoginRequest,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenResponse]:
    """
    Authenticate user with email and password and provide access token and refresh token.

    **Request body (JSON):**
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
    Returns:
        TokenResponse : Access token and refresh token if authentication is successful, None otherwise.
    """

    user = await AuthenticateUserByEmailPassword(user_repository).execute(credentials.email, credentials.password)

    user_role = UserRole(user.role).name.lower()

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()

    result = SuccessResult[TokenResponse](
        code=SuccessCodes.CREATED,
        message="Tokens created successfully",
        status_code=status.HTTP_201_CREATED,
        data=tokens,
    )

    return result.to_json_response(request)


@router.post(
    "/token/swagger",
    response_model=OAuth2TokenResponse,
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
):
    """
    **OAuth2-compliant token endpoint for Swagger UI.**

    Returns tokens in OAuth2 standard format (RFC 6749).
    This endpoint is specifically for Swagger UI's "Authorize" button.

    **Note:** This endpoint is disabled in production environments.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        user_repo (UserRepositoryInterface): User repository dependency.
    Returns:
        dict: Access token and token type.
    """

    email = form_data.username
    password = form_data.password

    print(f"Authenticating user with email: {email}", flush=True)
    print(f"Password provided: {password}", flush=True)

    user = await AuthenticateUserByEmailPassword(user_repo).execute(form_data.username, form_data.password)
    user_role = UserRole(user.role).name.lower()

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()

    return {"access_token": tokens.access_token, "token_type": "bearer"}


@router.get(
    "/me",
    description="Get current user information",
    # SuccessResponse[UserRead]
    response_model=None,
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
    return result.to_json_response(request)


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
    payload: JWTPayload = await ReadJwtToken(refresh_token).execute()

    user = await VerifyTokenPayload(user_repository).execute(payload, TokenType.refresh)
    user_role = UserRole(user.role).name.lower()

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()
    result = SuccessResult[TokenResponse](
        code=SuccessCodes.CREATED,
        message="Tokens created successfully",
        status_code=status.HTTP_201_CREATED,
        data=tokens,
    )

    return result.to_json_response(request)


@router.get(
    "/token/verify",
    description="Verify access token",
    response_model=SuccessResponse[TokenResponse],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("access token verified successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_verify_refresh_token(
    request: Request,
    access_token: str,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenResponse]:
    """
    Verify access token.
    This endpoint allows the user to verify their access token.
    Args:
        request (Request): The FastAPI request object.
        user (UserRead): The authenticated user object.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        SuccessResponse[TokenResponse]: A success response containing the verified tokens.
    """
    payload: JWTPayload = await ReadJwtToken(access_token).execute()

    user_read = await VerifyTokenPayload(user_repository).execute(payload, TokenType.access)

    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User is valid",
        status_code=status.HTTP_200_OK,
        data=user_read,
    )

    return result.to_json_response(request)
