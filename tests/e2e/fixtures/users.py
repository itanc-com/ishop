import pytest

from ..data.users import USER_INVALID_EMAIL, USER_NORMAL, USER_WEAK_PASSWORD


@pytest.fixture
def normal_user_data():
    return USER_NORMAL


@pytest.fixture
def weak_password_user_data():
    return USER_WEAK_PASSWORD


@pytest.fixture
def invalid_email_user_data():
    return USER_INVALID_EMAIL
