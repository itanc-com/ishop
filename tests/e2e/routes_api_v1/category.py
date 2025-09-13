from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


def post_category(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/categories", headers=HEADER_JSON, data=data)


def get_category(api_request_context: APIRequestContext, category_id) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/categories/{category_id}", headers=HEADER_JSON)


def get_categories(api_request_context: APIRequestContext) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/categories", headers=HEADER_JSON)
