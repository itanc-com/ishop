from logging import Logger

from app.modules.auth.routers import auth_get_token
from app.modules.auth.schemas import TokenResponse


def login_user_get_tokens(api_request_context, logger: Logger, user: dict) -> TokenResponse:
    response = auth_get_token(api_request_context, user)
    if response.status == 200:
        tokens_json = response.json()
        return TokenResponse(**tokens_json)

    logger.warning("USER TOKENS NOT VALID")

    raise AssertionError
