import pytest

from ..data.users import USERS


@pytest.fixture
def normal_user_data():
    return USERS["normal"]

@pytest.fixture
def weak_password_user_data():
    return USERS["weak_password"]
