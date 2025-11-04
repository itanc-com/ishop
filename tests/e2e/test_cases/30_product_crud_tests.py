from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.product import LIST_PRODUCT, SAMPLE_PRODUCT, UPDATED_SAMPLE_PRODUCT
from tests.e2e.routes_api_v1.product import (
    delete_product,
    get_product,
    list_paginated_products,
    post_product,
    update_product,
)


@pytest.mark.order(30)
def test_create_product_success(api_request_context: APIRequestContext, logger: Logger):
    response = post_product(api_request_context, data=SAMPLE_PRODUCT)
    code = response.json().get("code")
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    assert code == "CREATED", f"Expected code 'CREATED', got {code}"
    logger.info(response.json().get("message"))


@pytest.mark.order(31)
def test_get_product_success(api_request_context: APIRequestContext, logger: Logger):
    response = get_product(api_request_context, product_id=1)
    code = response.json().get("code")
    data = response.json().get("data")
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    assert code == "SUCCESS", f"Expected code 'SUCCESS', got {code}"

    # Check that all fields from SAMPLE_PRODUCT are present in the response data
    for key, expected_value in SAMPLE_PRODUCT.items():
        assert key in data, f"Expected key '{key}' to be in response data"
        actual_value = data[key]
        assert actual_value == expected_value, f"Expected {key}='{expected_value}', got '{actual_value}'"

    logger.info(response.json().get("message"))


@pytest.mark.order(32)
def test_update_product_success(api_request_context: APIRequestContext, logger: Logger):
    response = update_product(api_request_context, data=UPDATED_SAMPLE_PRODUCT, product_id=1)
    code = response.json().get("code")
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    assert code == "SUCCESS", f"Expected code 'SUCCESS', got {code}"
    logger.info(response.json().get("message"))


@pytest.mark.order(33)
def test_delete_product_success(api_request_context: APIRequestContext, logger: Logger):
    response = delete_product(api_request_context, product_id=1)
    code = response.json().get("code")
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    assert code == "SUCCESS", f"Expected code 'SUCCESS', got {code}"
    logger.info(response.json().get("message"))


@pytest.mark.order(34)
def test_get_paginated_list_products(api_request_context: APIRequestContext, logger: Logger):
    # Create all products from LIST_PRODUCT
    for product in LIST_PRODUCT:
        post_product(api_request_context, data=product)

    # Test pagination with page=1, per_page=5
    response = list_paginated_products(api_request_context, page=1, limit=5)
    code = response.json().get("code")
    data = response.json().get("data")

    # Validate response structure
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    assert code == "SUCCESS", f"Expected code 'SUCCESS', got {code}"
    assert "items" in data, "Expected 'items' in response data"
    assert "pagination" in data, "Expected 'pagination' in response data"

    # Validate items
    items = data["items"]
    assert len(items) == 5, f"Expected 5 items on page 1, got {len(items)}"

    # Validate pagination info
    pagination = data["pagination"]
    assert pagination["page"] == 1, f"Expected page=1, got {pagination['page']}"
    assert pagination["limit"] == 5, f"Expected limit=5, got {pagination['limit']}"
    assert pagination["total_items"] == 21, f"Expected total_items=21, got {pagination['total_items']}"
    assert pagination["total_pages"] == 5, f"Expected total_pages=5, got {pagination['total_pages']}"
    assert not pagination["has_prev"], f"Expected has_prev=False for page 1, got {pagination['has_prev']}"
    assert pagination["has_next"], f"Expected has_next=True for page 1, got {pagination['has_next']}"

    logger.info(f"Successfully validated pagination: {pagination}")
    logger.info(f"Retrieved {len(items)} items for page 1")
