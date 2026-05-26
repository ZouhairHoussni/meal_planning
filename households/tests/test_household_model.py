from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from households.models import Household


@pytest.mark.django_db
def test_household_defaults_to_eur_and_two_servings(django_user_model):
    user = django_user_model.objects.create_user(username="household-user", password="test-pass-123")

    household = Household.objects.create(owner=user, name="Home", default_weekly_budget="80.00")
    household.refresh_from_db()

    assert household.currency == "EUR"
    assert household.default_servings == 2
    assert household.default_weekly_budget == Decimal("80.00")


@pytest.mark.django_db
def test_household_requires_positive_budget(django_user_model):
    user = django_user_model.objects.create_user(username="budget-validation", password="test-pass-123")
    household = Household(owner=user, name="Home", default_weekly_budget="0.00")

    with pytest.raises(ValidationError):
        household.full_clean()


@pytest.mark.django_db
def test_household_requires_positive_servings(django_user_model):
    user = django_user_model.objects.create_user(username="serving-validation", password="test-pass-123")
    household = Household(owner=user, name="Home", default_weekly_budget="80.00", default_servings=0)

    with pytest.raises(ValidationError):
        household.full_clean()


@pytest.mark.django_db
def test_user_can_only_own_one_mvp_household(django_user_model):
    user = django_user_model.objects.create_user(username="single-household", password="test-pass-123")
    Household.objects.create(owner=user, name="Home", default_weekly_budget="80.00")

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Household.objects.create(owner=user, name="Second home", default_weekly_budget="60.00")
