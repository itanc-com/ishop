import json

from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


def post_cart(api_request_context: APIRequestContext, data, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.post(f"{API_URL_V1}/cart", headers=headers, data=data)


def post_cart_item(api_request_context: APIRequestContext, data: dict, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.post(f"{API_URL_V1}/cart/items", headers=headers, data=json.dumps(data))


def update_cart_item(
    api_request_context: APIRequestContext, cart_item_id: int, data, auth_headers: dict
) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.put(f"{API_URL_V1}/cart/items/{cart_item_id}", headers=headers, data=json.dumps(data))


def get_cart_item(api_request_context: APIRequestContext, cart_item_id: int, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.get(f"{API_URL_V1}/cart/item/{cart_item_id}", headers=headers)


def delete_cart_item(
    api_request_context: APIRequestContext, user_id: str, product_id: int, auth_headers: dict
) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.delete(f"{API_URL_V1}/cart/items/user/{user_id}/item/{product_id}", headers=headers)


def get_cart(api_request_context: APIRequestContext, user_id: str, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.get(f"{API_URL_V1}/cart/item", headers=headers, params={"user_id": user_id})


def clear_cart(api_request_context: APIRequestContext, user_id: str, auth_headers: dict) -> APIResponse:
    headers = {**HEADER_JSON, **auth_headers}
    return api_request_context.delete(f"{API_URL_V1}/cart/item", headers=headers, params={"user_id": user_id})
