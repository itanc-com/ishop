import json
from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.product import PRODUCT_DATA, UPDATE_PRODUCT_DATA
from tests.e2e.routes_api_v1.product import delete_product, post_product, update_product


@pytest.mark.order(1)
def _test_product_creation_returns_expected_fields(
    api_request_context: APIRequestContext, logger: Logger, create_category_fixture
):
    category_id = create_category_fixture["id"]

    create_response = post_product(api_request_context, {**PRODUCT_DATA, "category_id": category_id})
    assert create_response.status == 201, f"Expected 201 Created, got {create_response.status}"

    created_product = create_response.json()["data"]
    # logger.info(created_product)

    assert created_product["title"] == PRODUCT_DATA["title"]
    assert created_product["price"] == PRODUCT_DATA["price"]
    assert created_product["sku"] == PRODUCT_DATA["sku"]


@pytest.mark.order(2)
def _test_product_update_applies_new_values(
    api_request_context: APIRequestContext, logger: Logger, create_category_fixture
):
    category_id = create_category_fixture["id"]

    create_response = post_product(api_request_context, {**PRODUCT_DATA, "category_id": category_id})
    assert create_response.status == 201, f"Expected 201 Created, got {create_response.status}"
    created_product = create_response.json()["data"]

    update_response = update_product(api_request_context, created_product["id"], UPDATE_PRODUCT_DATA)
    assert update_response.status == 200, f"Expected 200 OK, got {update_response.status}"

    updated_product = update_response.json()["data"]
    # logger.info(updated_product)

    assert updated_product["title"] == UPDATE_PRODUCT_DATA["title"]
    assert updated_product["price"] == UPDATE_PRODUCT_DATA["price"]
    assert updated_product["sku"] == UPDATE_PRODUCT_DATA["sku"]


@pytest.mark.order(3)
def _test_product_deletion_returns_deleted_data(
    api_request_context: APIRequestContext, logger: Logger, create_category_fixture
):
    category_id = create_category_fixture["id"]

    create_response = post_product(api_request_context, {**PRODUCT_DATA, "category_id": category_id})
    assert create_response.status == 201, f"Expected 201 Created, got {create_response.status}"
    created_product = create_response.json()["data"]

    delete_response = delete_product(api_request_context, created_product["id"])
    assert delete_response.status == 200, f"Expected 200 OK, got {delete_response.status}"

    deleted_product_data = json.loads(delete_response.headers["x-deleted-product"])
    # logger.info(deleted_product_data)

    assert deleted_product_data["title"] == PRODUCT_DATA["title"]
    assert deleted_product_data["sku"] == PRODUCT_DATA["sku"]
