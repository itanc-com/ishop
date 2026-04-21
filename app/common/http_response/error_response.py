from enum import StrEnum
from typing import Any

from pydantic import BaseModel

from .base import BaseResponse


class ErrorCodes(StrEnum):
    CONFLICT = "CONFLICT"
    BAD_REQUEST = "BAD_REQUEST"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_MEDIA = "INVALID_MEDIA"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    INVALID_TOKEN = "INVALID_TOKEN"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    INTERNAL_SERVER = "INTERNAL_SERVER"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"


class ErrorResponse(BaseResponse):
    """
    ErrorResponse represents the structure of an error response returned by the API, Inspired by RFC 7807.

    Attributes:
        code (str): A short string representing the error code.
        message (str): A detailed description of the error.
        status (int): The HTTP status code associated with the error.
        timestamp (datetime): The timestamp when the error occurred.
        path (str): The request path that caused the error.
        data (dict[str, Any] | None): Optional additional data related to the error.
    """

    code: ErrorCodes
    data: dict[str, Any] | None = None


class ErrorResponseWrapper(BaseModel):
    detail: ErrorResponse
