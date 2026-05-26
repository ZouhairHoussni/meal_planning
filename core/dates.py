from datetime import date, timedelta

from django.utils import timezone


def monday_for_date(value: date) -> date:
    return value - timedelta(days=value.weekday())


def current_week_start(value: date | None = None) -> date:
    return monday_for_date(value or timezone.localdate())
