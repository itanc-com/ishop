from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.common.exceptions.app_exceptions import AuthenticationException
from app.common.http_response.error_response import ErrorCodes
from app.core.config.constants import AUTH_TOKEN_SWAGGER


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        try:
            return await super().__call__(request)
        except HTTPException as e:
            raise AuthenticationException(code=ErrorCodes.UNAUTHORIZED, message="Not authenticated", data=None) from e


oauth2_bearer = CustomOAuth2PasswordBearer(
    tokenUrl=AUTH_TOKEN_SWAGGER,
)
