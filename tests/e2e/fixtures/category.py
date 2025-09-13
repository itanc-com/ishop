import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.category import CATEGORY_DATA
from tests.e2e.routes_api_v1.category import post_category


@pytest.fixture
def create_category_fixture(api_request_context: APIRequestContext):
    response = post_category(api_request_context, CATEGORY_DATA)
    assert response.status == 201
    return response.json()["data"]
