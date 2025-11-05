from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.users import USER_NORMAL
from tests.e2e.routes_api_v1.users import post_register_user


@pytest.mark.order(1)
def test_register_user_success(api_request_context: APIRequestContext, logger: Logger):
    response = post_register_user(api_request_context, USER_NORMAL)
    code = response.json().get("code")
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    assert code == "CREATED", f"Expected code 'CREATED', got {code}"
    logger.info(response.json().get("message"))


@pytest.mark.order(2)
def test_register_user_duplicate_email_conflict(api_request_context: APIRequestContext, logger: Logger):
    response = post_register_user(api_request_context, USER_NORMAL)
    json_data = response.json()
    code = json_data.get("detail", {}).get("code")
    assert (
        response.status == 409 and code == "DUPLICATE_ENTRY"
    ), f"Expected 409 Conflict with code 'DUPLICATE_ENTRY', got {response.status} and {code}"


@pytest.mark.order(3)
def test_create_user_invalid_email(api_request_context: APIRequestContext, logger: Logger):
    invalid_email_user_data = {**USER_NORMAL, "email": "invalid-email"}
    response = post_register_user(api_request_context, invalid_email_user_data)
    json_data = response.json()
    err_type = json_data.get("detail", [{}])[0].get("type")
    err_input = json_data.get("detail", [{}])[0].get("input")
    assert response.status == 422, f"Expected 422 Unprocessable Entity, got {response.status}"
    assert err_type == "value_error", f"Expected error type 'value_error', got {err_type}"
    assert err_input == "invalid-email", f"Expected input 'invalid-email', got {err_input}"


@pytest.mark.order(4)
def test_register_user_weak_password_validation(api_request_context: APIRequestContext, logger: Logger):
    weak_password_user_data = {**USER_NORMAL, "password": "123"}
    response = post_register_user(api_request_context, weak_password_user_data)
    json_data = response.json()
    err_type = json_data.get("detail", [{}])[0].get("type")
    err_input = json_data.get("detail", [{}])[0].get("input")
    assert response.status == 422, f"Expected 422 Unprocessable Entity, got {response.status}"
    assert err_type == "string_too_short", f"Expected error type 'string_too_short', got {err_type}"
    assert err_input == "123", f"Expected input '123', got {err_input}"
