import json

from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


def get_cart(api_request_context: APIRequestContext, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.get(f"{API_URL_V1}/cart", headers=headers)


def post_cart(api_request_context: APIRequestContext, data, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.post(f"{API_URL_V1}/cart", headers=headers, data=data)


def post_cart_items(api_request_context: APIRequestContext, data: dict, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.post(f"{API_URL_V1}/cart/items", headers=headers, data=json.dumps(data))


def put_cart_items_one(
    api_request_context: APIRequestContext, product_id: int, data, auth_headers: dict
) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.put(f"{API_URL_V1}/cart/items/{product_id}", headers=headers, data=json.dumps(data))


def get_cart_items_one(api_request_context: APIRequestContext, product_id: int, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.get(f"{API_URL_V1}/cart/items/{product_id}", headers=headers)


def delete_cart_items_one(api_request_context: APIRequestContext, product_id: int, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.delete(f"{API_URL_V1}/cart/items/{product_id}", headers=headers)


def delete_cart_items(api_request_context: APIRequestContext, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.delete(f"{API_URL_V1}/cart/items", headers=headers)


def post_sync_cart(api_request_context: APIRequestContext, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.post(f"{API_URL_V1}/cart/items/sync", headers=headers)
