import datetime

from app.common.http_response.error_response import ErrorCodes, ErrorResponse


class AppBaseException(Exception):
    def __init__(self, *, code: ErrorCodes, message: str, status_code: int = 400, data: dict | None = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}

    def to_response_model(self, path: str = "") -> ErrorResponse:
        return ErrorResponse(
            # type=f"https://api.example.com/errors/{self.code.value.lower()}", !# not needed for now
            code=self.code,
            message=self.message,
            status=self.status_code,
            timestamp=datetime.datetime.now(datetime.timezone.utc),  # RFC 3339-compliant
            path=path,
            data=self.data,
        )


class InternalServerException(AppBaseException):
    """
    Raised when an unexpected server error occurs (500 Internal Server Error).

    Use cases:
    - Database connection failures
    - Unexpected exceptions during request processing
    - External API failures
    - File system errors
    - Configuration errors
    """

    def __init__(
        self,
        code: ErrorCodes = ErrorCodes.INTERNAL_SERVER,
        message: str = "An internal server error occurred",
        data: dict | None = None,
    ):
        if data is None:
            data = {}
        super().__init__(
            code=code,
            message=message,
            status_code=500,
            data=data,
        )


class BadRequestException(AppBaseException):
    """
    Raised when the client sends an invalid request (400 Bad Request).

    Use cases:
    - Malformed JSON payload
    - Missing required fields
    - Invalid query parameters
    - Data validation errors
    - Unsupported media types
    """

    def __init__(
        self,
        code: ErrorCodes = ErrorCodes.BAD_REQUEST,
        message: str = "Bad request",
        data: dict | None = None,
    ):
        if data is None:
            data = {}
        super().__init__(
            code=code,
            message=message,
            status_code=400,
            data=data,
        )


class AuthenticationException(AppBaseException):
    """
    Raised when authentication fails (401 Unauthorized).

    Use cases:
    - Invalid or missing authentication token
    - Expired token
    - Invalid credentials (wrong email/password)
    - Invalid JWT payload
    - Token signature verification failed
    """

    def __init__(
        self,
        code: ErrorCodes = ErrorCodes.UNAUTHORIZED,
        message: str = "Authentication fails",
        data: dict | None = None,
    ):
        if data is None:
            data = {}
        super().__init__(
            code=code,
            message=message,
            status_code=401,
            data=data,
        )


class ForbiddenAccessException(AppBaseException):
    """
    Raised when user lacks permission to access a resource (403 Forbidden).

    Use cases:
    - Insufficient role/permissions
    - Accessing another user's resources
    - Admin-only endpoints accessed by regular users
    - Account suspended or disabled
    """

    def __init__(self, data=None, message: str = "You do not have permission to access this resource"):
        if data is None:
            data = {}
        super().__init__(
            code=ErrorCodes.FORBIDDEN,
            message=message,
            status_code=403,
            data=data,
        )


class ConflictException(AppBaseException):
    """
    Raised when a request conflicts with the current state (409 Conflict).

    Use cases:
    - Duplicate email during user registration
    - Duplicate username or phone number
    - Version conflict (optimistic locking)
    - Resource state conflict (e.g., canceling already shipped order)
    - Concurrent modification conflicts
    """

    def __init__(
        self,
        code: ErrorCodes = ErrorCodes.CONFLICT,
        message: str = "Request conflicts with the current state",
        data: dict | None = None,
    ):
        if data is None:
            data = {}

        super().__init__(
            code=code,
            message=message,
            status_code=409,
            data=data,
        )


class NotFoundException(AppBaseException):
    """
    Raised when a requested resource is not found (404 Not Found).

    Use cases:
    - User not found by ID or email
    - Product not found by ID or SKU
    - Order not found
    - Category not found
    - Cart item not found
    - Invalid endpoint/route
    """

    def __init__(
        self,
        code: ErrorCodes = ErrorCodes.RESOURCE_NOT_FOUND,
        message: str = "Resource not found",
        data: dict | None = None,
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=404,
            data=data,
        )
