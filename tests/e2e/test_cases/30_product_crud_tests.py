from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.product import LIST_PRODUCT, SAMPLE_PRODUCT, UPDATED_SAMPLE_PRODUCT
from tests.e2e.routes_api_v1.product import delete_product, get_product, list_products, post_product, update_product


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
def test_get_list_products(api_request_context: APIRequestContext, logger: Logger):
    for product in LIST_PRODUCT:
        post_product(api_request_context, data=product)

    response = list_products(api_request_context)

    logger.info(response.json())
