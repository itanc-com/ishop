import pytest

from tests.e2e.routes_api_v1.users import post_register_user
from tests.e2e.data.users import USERS


def test_create_user_success(api_request_context, normal_user_data):
    response = post_register_user(api_request_context, normal_user_data)
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    json_data = response.json()
    data = json_data.get("data", {})
    assert "id" in data
    assert data["email"] == normal_user_data["email"]


def test_create_user_duplicate_email(api_request_context, normal_user_data):
    post_register_user(api_request_context, normal_user_data)
    response = post_register_user(api_request_context, normal_user_data)
    assert response.status == 409
    error_message = response.json().get("detail", {}).get("message", "")
    assert "already exists" in error_message


def test_create_user_invalid_email(api_request_context, invalid_email_user_data):
    response = post_register_user(api_request_context, invalid_email_user_data)
    assert response.status == 422  # Validation error
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    assert any("value is not a valid email" in msg for msg in error_messages)


def test_create_user_weak_password(api_request_context, weak_password_user_data):
    response = post_register_user(api_request_context, weak_password_user_data)
    assert response.status == 422  # Validation error
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    assert any("at least 8 characters" in msg for msg in error_messages)
