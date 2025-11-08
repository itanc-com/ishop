from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


def post_cart(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/cart", headers=HEADER_JSON, data=data)


def post_cart_item(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/cart/item", headers=HEADER_JSON, data=data)


def update_cart_item(api_request_context: APIRequestContext, cart_item_id: int, data) -> APIResponse:
    return api_request_context.put(f"{API_URL_V1}/cart/item/{cart_item_id}", headers=HEADER_JSON, data=data)


def get_cart_item(api_request_context: APIRequestContext, cart_item_id: int) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/cart/item/{cart_item_id}", headers=HEADER_JSON)


def delete_cart_item(api_request_context: APIRequestContext, user_id: str, product_id: int) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/cart/items/user/{user_id}/item/{product_id}", headers=HEADER_JSON)


def get_cart(api_request_context: APIRequestContext, user_id: str) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/cart/item", headers=HEADER_JSON, params={"user_id": user_id})


def clear_cart(api_request_context: APIRequestContext, user_id: str) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/cart/item", headers=HEADER_JSON, params={"user_id": user_id})
