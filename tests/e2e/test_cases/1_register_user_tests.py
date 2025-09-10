from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.routes_api_v1.users import post_register_user

from ..data.users import USER_NORMAL


@pytest.mark.order(1)
def test_create_user_success(api_request_context: APIRequestContext, logger: Logger):
    response = post_register_user(api_request_context, USER_NORMAL)
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    json_data = response.json()
    data = json_data.get("data", {})
    # logger.info(data)
    assert "id" in data
    assert data["email"] == USER_NORMAL["email"]


@pytest.mark.order(2)
def test_create_user_duplicate_email(api_request_context: APIRequestContext, logger: Logger):
    post_register_user(api_request_context, USER_NORMAL)
    response = post_register_user(api_request_context, USER_NORMAL)
    assert response.status == 409, f"Expected 409 Conflict, got {response.status}"
    json_data = response.json()
    error_message = json_data.get("detail", {}).get("message", "")
    # logger.info(error_message)
    assert "already exists" in error_message


@pytest.mark.order(3)
def test_create_user_invalid_email(api_request_context: APIRequestContext, logger: Logger):
    invalid_email_user_data = {**USER_NORMAL, "email": "invalid-email"}
    response = post_register_user(api_request_context, invalid_email_user_data)
    assert response.status == 422, f"Expected 422 Unprocessable Entity, got {response.status}"
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    # logger.info(error_messages)
    assert any("value is not a valid email" in msg for msg in error_messages)


@pytest.mark.order(4)
def test_create_user_weak_password(api_request_context: APIRequestContext, logger: Logger):
    weak_password_user_data = {**USER_NORMAL, "password": "123"}
    response = post_register_user(api_request_context, weak_password_user_data)
    assert response.status == 422, f"Expected 422 Unprocessable Entity, got {response.status}"
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    # logger.info(error_messages)
    assert any("at least 8 characters" in msg for msg in error_messages)
