from datetime import UTC, datetime


def now():
    return datetime.now(UTC)

def today():
    return now().date()