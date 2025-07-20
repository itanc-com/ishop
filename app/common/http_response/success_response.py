from enum import StrEnum
from typing import Generic, TypeVar

from .base import BaseResponse

T = TypeVar("T")


class SuccessCodes(StrEnum):
    """Enum for success codes."""

    SUCCESS = "SUCCESS"  # 200
    CREATED = "CREATED"  # 201
    ACCEPTED = "ACCEPTED"  # 202
    NO_CONTENT = "NO_CONTENT"  # 204


class SuccessResponse(BaseResponse, Generic[T]):
    """
    SuccessResponse represents the structure of a successful response returned by the API.

    Attributes:
        code (SuccessCodes): A short string representing the success code.
        data (T): The data returned in the response, which is a Pydantic model.
        message (str): A detailed description of the success response.
        status (int): The HTTP status code associated with the response.
        timestamp (datetime): The timestamp when the response was generated.
        path (str): The request path that generated the response.
    """

    code: SuccessCodes
    data: T | None = None
