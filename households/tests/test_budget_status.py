from decimal import Decimal

import pytest

from households.models import Household
from households.selectors import budget_status_for_user
from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_budget_status_shows_remaining_known_spend(django_user_model):
    user = django_user_model.objects.create_user(username="budget-user", password="test-pass-123")
    household = Household.objects.create(owner=user, name="Budget home", default_weekly_budget="80.00")
    ShoppingItem.objects.create(owner=user, name="Pasta", quantity="1", unit="unit", price="12.50")

    status = budget_status_for_user(user, household)

    assert status.budget == Decimal("80.00")
    assert status.known_spend == Decimal("12.50")
    assert status.remaining == Decimal("67.50")
    assert status.is_over_budget is False


@pytest.mark.django_db
def test_budget_status_marks_over_budget(django_user_model):
    user = django_user_model.objects.create_user(username="over-budget-user", password="test-pass-123")
    household = Household.objects.create(owner=user, name="Budget home", default_weekly_budget="10.00")
    ShoppingItem.objects.create(owner=user, name="Coffee", quantity="1", unit="unit", price="12.50")

    status = budget_status_for_user(user, household)

    assert status.remaining == Decimal("-2.50")
    assert status.is_over_budget is True
    assert status.display_delta == Decimal("2.50")
