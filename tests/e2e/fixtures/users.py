import uuid

import pytest


@pytest.fixture
def unique_user_data():
    unique_suffix = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"testuser_{unique_suffix}@example.com",
        "password": "StrongPass123!",
    }
    return user_data
