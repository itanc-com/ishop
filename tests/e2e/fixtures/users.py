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


@pytest.fixture
def registered_user(api_request_context: APIRequestContext):
    response = post_register_user(api_request_context, USER_NORMAL)
    data = response.json().get("data", {})
    return response, data
