from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


# POST /api_v1/users/
def post_register_user(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/users/", headers=HEADER_JSON, data=data)


# DELETE /api_v1/users/delete_by_email
def delete_user_by_email(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/users/delete_by_email", headers=HEADER_JSON, params=data)
