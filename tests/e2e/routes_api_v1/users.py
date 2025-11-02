from playwright.sync_api import APIRequestContext, APIResponse

from ..config import API_URL_V1
from ..data.headers import HEADER_JSON


# Get /api_v1/users/{user_id}
def get_user_by_id(api_request_context: APIRequestContext, user_id) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/users/{user_id}", headers=HEADER_JSON)


# GET /api_v1/users/by_email/{user_email}
def get_user_by_email(api_request_context: APIRequestContext, user_email) -> APIResponse:
    return api_request_context.get(f"{API_URL_V1}/users/by_email/{user_email}", headers=HEADER_JSON)


# POST /api_v1/users/
def post_register_user(api_request_context: APIRequestContext, data) -> APIResponse:
    return api_request_context.post(f"{API_URL_V1}/users/", headers=HEADER_JSON, data=data)


# DELETE /api_v1/users/{user_id}
def delete_user_by_id(api_request_context: APIRequestContext, user_id) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/users/{user_id}", headers=HEADER_JSON)


# DELETE /api_v1/users/by_email/{user_email}
def delete_user_by_email(api_request_context: APIRequestContext, user_email) -> APIResponse:
    return api_request_context.delete(f"{API_URL_V1}/users/by_email/{user_email}", headers=HEADER_JSON)
