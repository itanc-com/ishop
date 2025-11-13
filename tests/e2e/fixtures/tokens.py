from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from app.modules.auth.routers import auth_get_token
from app.modules.auth.schemas import TokenResponse


def login_user_get_tokens(api_request_context, logger: Logger, user: dict) -> TokenResponse:
    response = auth_get_token(api_request_context, user)
    if response.status == 200:
        tokens_json = response.json()
        return TokenResponse(**tokens_json)

    logger.warning("USER TOKENS NOT VALID")

    raise AssertionError


@pytest.fixture(scope="session")
def logged_in_user(api_request_context: APIRequestContext) -> dict:
    """Login and return access token and user data."""
    from tests.e2e.data.users import USER_NORMAL
    from tests.e2e.routes_api_v1.auth import post_login

    login_data = {"email": USER_NORMAL["email"], "password": USER_NORMAL["password"]}
    response = post_login(api_request_context, login_data)

    assert response.status == 201, f"Login failed: {response.status}"

    data = response.json().get("data", {})
    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_type": data.get("token_type", "bearer"),
    }


@pytest.fixture(scope="session")
def auth_headers(logged_in_user: dict) -> dict:
    """Return authorization headers with Bearer token."""
    return {
        "Authorization": f"{logged_in_user['token_type']} {logged_in_user['access_token']}",
        "Content-Type": "application/json",
    }
