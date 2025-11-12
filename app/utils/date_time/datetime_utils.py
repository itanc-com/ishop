"""
This module uses datetime.UTC and is compatible with Python 3.12+.
All timezone operations assume Python 3.12 or newer.
"""

from datetime import UTC, datetime


def to_utc(dt: datetime) -> datetime:
    """Convert a naive or local datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def get_utc_now() -> datetime:
    """Get the current UTC datetime."""
    return datetime.now(UTC).replace(microsecond=0)


def get_current_utc(include_microseconds: bool = False) -> datetime:
    """
    Get current UTC datetime object with optional microsecond precision.

    Args:
        include_microseconds: If True, includes microseconds. If False, sets to 0.

    Returns:
        datetime object (timezone-aware UTC)

    Examples:
        >>> dt = get_current_utc_datetime()
        datetime.datetime(2025, 11, 12, 14, 30, 45, tzinfo=datetime.timezone.utc)

        >>> dt = get_current_utc_datetime(include_microseconds=True)
        datetime.datetime(2025, 11, 12, 14, 30, 45, 123456, tzinfo=datetime.timezone.utc)
    """
    now = datetime.now(UTC)

    if not include_microseconds:
        now = now.replace(microsecond=0)

    return now
