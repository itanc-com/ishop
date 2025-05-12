class BaseException(Exception):
    """Base class for other custom exceptions."""

    pass


class CredentialsException(BaseException):
    """Raised when ."""

    def __init__(self, message="Invalid credentials"):
        super().__init__(message)


class DuplicateEntryException(BaseException):
    def __init__(self, field: str = "Entry", value: str = "", message: str = None):
        if not message:
            message = f"{field} '{value}' already exists"
        super().__init__(message)
