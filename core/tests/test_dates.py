from datetime import date

from django.utils import timezone

from core.dates import current_week_start, monday_for_date


def test_monday_for_date_returns_monday_start():
    assert monday_for_date(date(2026, 5, 25)) == date(2026, 5, 25)
    assert monday_for_date(date(2026, 5, 31)) == date(2026, 5, 25)


def test_current_week_start_uses_configured_timezone():
    assert timezone.get_default_timezone_name() == "Europe/Paris"
    assert current_week_start(date(2026, 5, 26)) == date(2026, 5, 25)
