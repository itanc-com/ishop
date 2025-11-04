from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


def post_product(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/products", headers=HEADER_JSON, data=data)


def get_product(api_request_context: APIRequestContext, product_id: int) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/products/{product_id}", headers=HEADER_JSON)


def update_product(api_request_context: APIRequestContext, data, product_id) -> APIResponse:
    return api_request_context.put(f"{API_URL_V1}/products/{product_id}", headers=HEADER_JSON, data=data)


def delete_product(api_request_context: APIRequestContext, product_id) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/products/{product_id}", headers=HEADER_JSON)


def list_paginated_products(api_request_context: APIRequestContext, page: int, limit: int) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/products", headers=HEADER_JSON, params={"page": page, "limit": limit})


def list_paginated_products_per_category(
    api_request_context: APIRequestContext, category_id: int, page: int, limit: int
) -> APIResponse:
    return api_request_context.get(
        f"{API_URL_V1}/products", headers=HEADER_JSON, params={"category_id": category_id, "page": page, "limit": limit}
    )
