from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_FORM_URLENCODED


def post_login(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/auth/token", headers={**HEADER_FORM_URLENCODED}, form=data)
