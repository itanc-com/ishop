from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.category import CATEGORY_DATA
from tests.e2e.routes_api_v1.category import get_categories, get_category, post_category


@pytest.mark.order(1)
def test_category_creation_returns_expected_fields(api_request_context: APIRequestContext, logger: Logger):
    response = post_category(api_request_context, CATEGORY_DATA)
    assert response.status == 201, f"Expected 201 Created, got {response.status}"

    created_category = response.json()["data"]
    # logger.info(created_category)

    assert "id" in created_category
    assert created_category["title"] == CATEGORY_DATA["title"]


@pytest.mark.order(2)
def test_category_retrieval_returns_correct_data(api_request_context: APIRequestContext, logger: Logger):
    create_response = post_category(api_request_context, CATEGORY_DATA)
    assert create_response.status == 201, f"Expected 201 Created, got {create_response.status}"
    created_category = create_response.json()["data"]

    retrieve_response = get_category(api_request_context, created_category["id"])
    assert retrieve_response.status == 200, f"Expected 200 OK, got {retrieve_response.status}"
    retrieved_category = retrieve_response.json()["data"]
    # logger.info(retrieved_category)

    assert retrieved_category["id"] == created_category["id"]
    assert retrieved_category["title"] == created_category["title"]


@pytest.mark.order(3)
def test_list_categories(api_request_context: APIRequestContext, logger: Logger):
    post_category(api_request_context, CATEGORY_DATA)
    post_category(api_request_context, CATEGORY_DATA)
    post_category(api_request_context, CATEGORY_DATA)

    categories_response = get_categories(api_request_context)
    assert categories_response.status == 200, f"Expected 200 OK, got {categories_response.status}"
    categories_data = categories_response.json()["data"]
    logger.info(categories_data)

    assert len(categories_data) >= 3, f"Expected at least 3 categories, got {len(categories_data)}"
