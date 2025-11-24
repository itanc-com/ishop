import pytest
from playwright.sync_api import APIRequestContext

from ..data.users import USER_INVALID_EMAIL, USER_NORMAL, USER_WEAK_PASSWORD
from ..routes_api_v1.users import post_register_user


@pytest.fixture
def normal_user_data():
    return USER_NORMAL


@pytest.fixture
def weak_password_user_data():
    return USER_WEAK_PASSWORD


@pytest.fixture
def invalid_email_user_data():
    return USER_INVALID_EMAIL


@pytest.fixture(scope="session")
def registered_user(api_request_context: APIRequestContext, normal_user_data):
    response = post_register_user(api_request_context, normal_user_data)

    # Assert registration succeeded
    assert response.status == 201, f"User registration failed: {response.status}"

    data = response.json().get("data", {})

    # Include plain password for login
    data["password"] = normal_user_data["password"]

    return response, data
