from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.routes_api_v1.cart import get_cart, post_cart_item


@pytest.mark.order(41)
def test_add_item_to_cart_success(api_request_context: APIRequestContext, logger: Logger, auth_headers: dict):
    product = {"product_id": 1, "quantity": 2}
    response = post_cart_item(api_request_context, data=product, auth_headers=auth_headers)

    logger.info(f"Response status: {response.status}")
    logger.info(f"Response text: {response.text()}")

    assert response.status == 201, f"Expected 201 Created, got {response.status}"

    response_data = response.json()
    logger.info(response_data.get("message"))


@pytest.mark.order(42)
def test_get_cart(api_request_context: APIRequestContext, auth_headers: dict, logger: Logger):
    response = get_cart(api_request_context, user_id="1", auth_headers=auth_headers)
    assert response.status == 200

    response_data = response.json()
    logger.info(response_data.get("message"))
