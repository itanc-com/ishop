class BaseException(Exception):
    """Base class for other custom exceptions."""

    pass


class CredentialsException(BaseException):
    """Raised when ."""

    def __init__(self, message="Invalid credentials"):
        super().__init__(message)


class UserEmailAlreadyExistsException(BaseException):
    """Raised when the email already exists."""

    def __init__(self, message="Email already exists"):
        super().__init__(message)
