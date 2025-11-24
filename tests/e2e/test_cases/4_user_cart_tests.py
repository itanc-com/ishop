from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from app.common.http_response.success_response import SuccessCodes
from tests.e2e.routes_api_v1.cart import (
    delete_cart_items_one,
    get_cart,
    post_cart_items,
)


@pytest.mark.order(401)
def test_add_item_to_cart_success(api_request_context: APIRequestContext, logger: Logger, auth_headers: dict):
    product = {"product_id": 1, "quantity": 2}
    response = post_cart_items(api_request_context, data=product, auth_headers=auth_headers)

    # logger.info(f"Response status: {response.status}")

    assert response.status == 201, f"Expected 201 Created, got {response.status}"

    response_data = response.json()
    logger.warning(f"Response text: {response_data})")

    logger.info(response_data.get("message"))


@pytest.mark.order(402)
def test_get_cart_success(api_request_context: APIRequestContext, auth_headers: dict, logger: Logger):
    response = get_cart(api_request_context, auth_headers=auth_headers)

    assert response.status == 200
    response_data = response.json()
    data = response_data.get("data")
    total = data.get("total")

    assert total == 500.0, f"Expected total 500.0, got {total}"

    items = data.get("items")
    assert len(items) == 1, f"Expected 1 item in cart, got {len(items)}"


@pytest.mark.order(403)
def test_remove_item_from_cart_success(api_request_context: APIRequestContext, auth_headers: dict, logger: Logger):
    response = delete_cart_items_one(api_request_context, product_id=1, auth_headers=auth_headers)
    assert response.status == 200
    response_data = response.json()

    assert response_data.get("code") == SuccessCodes.SUCCESS

    logger.error(f"Response data: {response_data}")
