# clean up all product data
# clean up all category data
# clean up all order data
# clean up all cart data
# clean up all user data

from logging import Logger

import pytest
from playwright.sync_api import APIRequestContext

from tests.e2e.data.users import USER_NORMAL
from tests.e2e.routes_api_v1.users import delete_user_by_id, get_user_by_email


# test clean up all user data
@pytest.mark.order(900)
def test_delete_user_by_email(api_request_context: APIRequestContext, logger: Logger):
    # Clear users

    response_get_user = get_user_by_email(api_request_context, USER_NORMAL["email"])

    user_id = response_get_user.json().get("data").get("id")

    response_delete = delete_user_by_id(api_request_context, int(user_id))

    assert response_delete.status == 200, f"Expected 200 OK, got {response_delete.status}"
    assert (
        response_delete.json().get("code") == "SUCCESS"
    ), f"Expected code 'SUCCESS', got {response_delete.json().get('code')}"

    logger.info(response_delete.json().get("message"))
