from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.product import SAMPLE_PRODUCT
from tests.e2e.routes_api_v1.product import (
    post_product,
)


@pytest.mark.order(41)
def test_add_item_to_cart_success(api_request_context: APIRequestContext, logger: Logger):
    response = post_product(api_request_context, data=SAMPLE_PRODUCT)
    code = response.json().get("code")
    assert response.status == 201, f"Expected 201 Created, got {response.status}"
    assert code == "CREATED", f"Expected code 'CREATED', got {code}"
    logger.info(response.json().get("message"))
