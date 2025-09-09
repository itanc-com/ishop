from tests.e2e.routes_api_v1.users import post_register_user


def test_create_user_success(api_request_context, unique_user_data):
    response = post_register_user(api_request_context, unique_user_data)
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    json_data = response.json()
    data = json_data.get("data", {})
    assert "id" in data
    assert data["email"] == unique_user_data["email"]


def test_create_user_duplicate_email(api_request_context, unique_user_data):
    post_register_user(api_request_context, unique_user_data)
    response = post_register_user(api_request_context, unique_user_data)
    assert response.status == 409
    error_message = response.json().get("detail", {}).get("message", "")
    assert "already exists" in error_message


def test_create_user_invalid_email(api_request_context):
    user_data = {
        "email": "not-an-email",
        "password": "StrongPass123!",
        "username": "testuser_invalid_email"
    }
    response = post_register_user(api_request_context, user_data)
    assert response.status == 422  # Validation error
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    assert any("value is not a valid email" in msg for msg in error_messages)


def test_create_user_weak_password(api_request_context):
    user_data = {
        "email": "weakpass@example.com",
        "password": "123",
        "username": "testuser_weakpass"
    }
    response = post_register_user(api_request_context, user_data)
    assert response.status == 422  # Validation error
    json_data = response.json()
    assert "detail" in json_data
    error_messages = [err["msg"].lower() for err in json_data.get("detail", [])]
    assert any("at least 8 characters" in msg for msg in error_messages)
