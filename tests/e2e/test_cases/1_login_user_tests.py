from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from app.common.enums.user import UserStatus
from tests.e2e.data.users import USER_NORMAL
from tests.e2e.routes_api_v1.auth import post_login


@pytest.mark.order(1)
def _test_login_disabled_user(api_request_context: APIRequestContext, registered_user, logger: Logger):
    response, user_data = registered_user

    assert user_data["status"] == UserStatus.DEACTIVE

    login_data = {"username": USER_NORMAL["email"], "password": USER_NORMAL["password"]}

    login_response = post_login(api_request_context, login_data)

    logger.info(login_response.json())
    # assert login_response.status == 201, f"Expected 201 Created, got {login_response.status}"


@pytest.mark.order(2)
def _test_login_unverified_user(api_request_context: APIRequestContext, registered_user, logger: Logger):
    _, user_data = registered_user
    assert user_data["status"] != UserStatus.VERIFIED

    login_data = {"username": USER_NORMAL["email"], "password": USER_NORMAL["password"]}
    login_response = post_login(api_request_context, login_data)

    # logger.info(login_response.json())
    assert login_response.status == 201, f"Expected 201 Created, got {login_response.status}"


@pytest.mark.order(3)
def _test_login_with_wrong_password_fails(api_request_context: APIRequestContext, logger: Logger):
    login_data = {"username": USER_NORMAL["email"], "password": "WrongPass123!"}
    response = post_login(api_request_context, login_data)

    assert response.status == 401, f"Expected 401 Unauthorized, got {response.status}"

    error_message = response.json().get("detail", {}).get("message", "")
    # logger.info(error_message)

    assert "invalid" in error_message.lower()


@pytest.mark.order(4)
def test_login_with_correct_credentials(api_request_context: APIRequestContext, logger: Logger):
    login_data = {"email": USER_NORMAL["email"], "password": USER_NORMAL["password"]}
    response = post_login(api_request_context, login_data)

    # logger.debug(f"login data: {response.json()}")
    assert response.status == 201, f"Expected 201 Created, got {response.status}"

    json_data = response.json().get("data", {})
    # logger.info(json_data)

    assert "access_token" in json_data, "Login should return an access token"
