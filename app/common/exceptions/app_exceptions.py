import datetime

from .error_response import ErrorCodes, ErrorResponse


class AppBaseException(Exception):
    def __init__(
        self,
        *,
        code: ErrorCodes,
        message: str,
        status_code: int = 400,
        data: dict | None = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}

    def to_response_model(self, path: str = "") -> ErrorResponse:
        return ErrorResponse(
            #type=f"https://api.example.com/errors/{self.code.value.lower()}", !# not needed for now
            title=self.message,
            code=self.code,
            message=self.message,
            status=self.status_code,
            timestamp=datetime.datetime.now(datetime.timezone.utc), # RFC 3339-compliant
            path=path,
            data=self.data
        )
    
class InvalidTokenException(AppBaseException):
    """Raised when ."""

    def __init__(self, message="Invalid token",token: str = "No token provided"):
        super().__init__(
            code=ErrorCodes.INVALID_TOKEN,
            message=message,
            status_code=401,
            data={"token": token}
        )

class InvalidPayloadException(AppBaseException):
    """Raised when ."""

    def __init__(self, message="Invalid payload",payload: dict = {1:"No payload provided"}):
        super().__init__(
            code=ErrorCodes.INVALID_PAYLOAD,
            message=message,
            status_code=401,
            data={"payload": payload}
        )


class DuplicateEntryException(AppBaseException):
    def __init__(self, field: str, value: str):
        super().__init__(
            code=ErrorCodes.DUPLICATE_ENTRY,
            message=f"{field} '{value}' already exists.",
            status_code=409,
            data={field: value}
        )

class InvalidCredentialsException(AppBaseException):
    def __init__(self, data: dict = {}, message:str = "Authentication failed"):
        super().__init__(
            code=ErrorCodes.INVALID_CREDENTIALS,
            message=message,
            status_code=401,
            data=data
        )
