from enum import IntEnum


class CaseInsensitiveIntEnum(IntEnum):
    """Base Enum class that allows case-insensitive string matching."""

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.name.lower() == value.lower():
                    return member
        return None

    def __str__(self) -> str:
        """Return lowercase name when converted to string."""
        return self.name.lower()


class UserRole(CaseInsensitiveIntEnum):
    ADMIN = 1
    USER = 2


class UserStatus(CaseInsensitiveIntEnum):
    DEACTIVE = 0
    ACTIVE = 1
    VERIFIED = 2
    SUSPEND = 3
    DELETE = 4
