from typing import Any

from .error_models import ErrorMessage


class ResponseError:
    @staticmethod
    def HTTP_200_OK(description: str) -> dict:
        return {200: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_201_CREATED(description: str) -> dict:
        return {201: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_202_ACCEPTED(description: str) -> dict:
        return {202: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_203_NON_AUTHORITATIVE_INFORMATION(description: str) -> dict:
        return {203: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_204_NO_CONTENT(description: str, headers: dict[str, Any]) -> dict:
        return {204: {"description": description, "headers": headers}}

    @staticmethod
    def HTTP_400_BAD_REQUEST(description: str) -> dict:
        return {400: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_401_UNAUTHORIZED(description: str) -> dict:
        return {401: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_402_PAYMENT_REQUIRED(description: str) -> dict:
        return {402: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_403_FORBIDDEN(description: str) -> dict:
        return {403: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_404_NOT_FOUND(description: str) -> dict:
        return {404: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_405_METHOD_NOT_ALLOWED(description: str) -> dict:
        return {405: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_409_CONFLICT(description: str) -> dict:
        return {409: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_429_TOO_MANY_REQUESTS(description: str) -> dict:
        return {429: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_422_UNPROCESSABLE_ENTITY(description: str) -> dict:
        return {422: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_498_INVALID_TOKEN(description: str) -> dict:
        return {498: {"model": ErrorMessage, "description": description}}

    @staticmethod
    def HTTP_500_INTERNAL_SERVER_ERROR(description: str) -> dict:
        return {500: {"model": ErrorMessage, "description": description}}


### 4xx  Error Status Codes

# HTTP_405_METHOD_NOT_ALLOWED
# HTTP_406_NOT_ACCEPTABLE
# HTTP_407_PROXY_AUTHENTICATION_REQUIRED
# HTTP_408_REQUEST_TIMEOUT
# HTTP_409_CONFLICT
# HTTP_410_GONE
# HTTP_411_LENGTH_REQUIRED
# HTTP_412_PRECONDITION_FAILED
# HTTP_413_PAYLOAD_TOO_LARGE
# HTTP_414_URI_TOO_LONG
# HTTP_415_UNSUPPORTED_MEDIA_TYPE
# HTTP_416_RANGE_NOT_SATISFINSUPPORTED_MEDIA_TYPEABLE
# HTTP_417_EXPECTATION_FAILED


# ### 5xx Server Error Status Codes
# HTTP_500_INTERNAL_SERVER_ERROR
# HTTP_501_NOT_IMPLEMENTED
# HTTP_502_BAD_GATEWAY
# HTTP_503_SERVICE_UNAVAILABLE
# HTTP_504_GATEWAY_TIMEOUT
