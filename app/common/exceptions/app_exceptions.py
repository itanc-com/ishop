import datetime
from typing import Any

from app.common.http_response.error_response import ErrorCodes, ErrorResponse


class AppBaseException(Exception):
    """
    Base exception class for application-specific errors.

    Attributes:
        code (ErrorCodes): The error code representing the type of exception.
        message (str): A human-readable message describing the error.
        status_code (int): HTTP status code associated with the error (default: 400).
        data (dict | None): Optional additional data relevant to the error.

    Methods:
        to_response_model(path: str = "") -> ErrorResponse:
            Converts the exception into an ErrorResponse model, including the error code,
            message, status code, current UTC timestamp (RFC 3339-compliant), request path,
            and any additional data.
    """

    default_error_code: ErrorCodes | None = None
    default_message: str = "An error occurred"
    default_status_code: int = 400

    def __init__(
        self,
        *,
        code: ErrorCodes | None = None,
        message: str | None = None,
        data: dict[str, Any] | None = None,
    ):
        self.code = code or self.default_error_code
        self.message = message or self.default_message
        self.status_code = self.default_status_code
        self.data = data if data is not None else {}
        super().__init__(self.message)

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

    default_error_code = ErrorCodes.INTERNAL_SERVER
    default_message = "An internal server error occurred"
    default_status_code = 500


class ExternalServiceException(AppBaseException):
    """
    Exception raised when an external service call fails.
    This exception is typically used when an operation that relies on an external service,
    such as an API call, fails due to network issues, service unavailability, or other errors.
    """

    default_error_code = ErrorCodes.EXTERNAL_SERVICE_ERROR
    default_message = "An external service error occurred"
    default_status_code = 502


class BadRequestException(AppBaseException):
    """
    Exception raised when an invalid payload is encountered.

    Raised when a request cannot be processed due to a client error.
    such as when a request body is missing required fields,
    contains invalid data types, or fails validation checks.

    This includes:
    - Invalid or expired OAuth tokens
    - Malformed query parameters or request data
    - Failed integration with external services due to bad requests
      (e.g., sending invalid payloads to Google OAuth APIs)
    """

    default_error_code = ErrorCodes.BAD_REQUEST
    default_message = "Invalid request payload"
    default_status_code = 400


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

    default_error_code = ErrorCodes.UNAUTHORIZED
    default_message = "Authentication failed"
    default_status_code = 401


class ForbiddenAccessException(AppBaseException):
    """
    Raised when user lacks permission to access a resource (403 Forbidden).

    Use cases:
    - Insufficient role/permissions
    - Accessing another user's resources
    - Admin-only endpoints accessed by regular users
    - Account suspended or disabled
    """

    default_error_code = ErrorCodes.FORBIDDEN
    default_message = "You do not have permission to access this resource"
    default_status_code = 403


class OperationNotAllowedException(AppBaseException):
    """
    Exception raised when an operation is not permitted on a specific entity.
    This exception is typically used when an action is attempted that is not allowed
    for a given entity, such as deleting a verified user or modifying a locked resource.
    """

    default_error_code = ErrorCodes.OPERATION_NOT_ALLOWED
    default_message = "Operation not allowed"
    default_status_code = 405


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

    default_error_code = ErrorCodes.CONFLICT
    default_message = "Request conflicts with the current state"
    default_status_code = 409


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

    default_error_code = ErrorCodes.RESOURCE_NOT_FOUND
    default_message = "Resource not found"
    default_status_code = 404


class MediaValidationException(AppBaseException):
    """
    Raised when media content (images, videos, etc.) fails validation or cannot be processed.
    This exception is typically used when media does not meet the required format, size, or other validation criteria.

    Examples:
        - File is not a valid media type
        - Media dimensions or duration are too large/small
        - File size exceeds the allowed maximum
        - Unsupported media format
    """

    default_error_code = ErrorCodes.INVALID_MEDIA
    default_message = "The media content cannot be processed due to validation failure."
    default_status_code = 415


class BusinessLogicException(AppBaseException):
    """
    Raised when an operation violates business rules or domain constraints.

    Use cases:
    - Attempting to delete a vendor with active listings
    - Trying to withdraw funds below minimum balance
    - Booking overlapping time slots
    - Exceeding allowed quota or limits
    - State transition violations (e.g., canceling a completed order)

    Note: Use ValidationException for input format/type errors.
          Use this for valid input that violates business rules.

    Examples:
        raise BusinessLogicException(
            message="Cannot delete vendor with active listings",
            data={"vendor_id": 123, "active_listings": 5}
        )
    """

    default_error_code = ErrorCodes.BUSINESS_RULE_VIOLATION
    default_message = "Business rule violation"
    default_status_code = 422
