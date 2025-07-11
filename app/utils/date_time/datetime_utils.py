from datetime import datetime, timezone


def get_utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0)
