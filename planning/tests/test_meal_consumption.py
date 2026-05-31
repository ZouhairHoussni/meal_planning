from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse

from pantry.models import PantryItem
from planning.models import MealConsumption, PantryConsumptionEntry, PlannedMeal
from planning.selectors import is_planned_meal_due
from recipes.models import Recipe, RecipeComponent


def create_planned_meal(user, *, date="2026-05-25", meal_type=PlannedMeal.MealType.DINNER):
    recipe = Recipe.objects.create(owner=user, name="Pasta dinner")
    RecipeComponent.objects.create(recipe=recipe, name="Pasta", quantity="250", unit="g")
    RecipeComponent.objects.create(recipe=recipe, name="Tomato sauce", quantity="1", unit="unit")
    return PlannedMeal.objects.create(owner=user, recipe=recipe, date=date, meal_type=meal_type)


@pytest.mark.django_db
def test_confirming_cooked_meal_deducts_available_pantry_stock(client, django_user_model):
    user = django_user_model.objects.create_user(username="cook-meal", password="test-pass-123")
    meal = create_planned_meal(user)
    PantryItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g")
    PantryItem.objects.create(owner=user, name="Tomato sauce", quantity="2", unit="unit")
    client.force_login(user)

    response = client.post(
        reverse("planner_outcome", kwargs={"pk": meal.pk}),
        {"action": "cooked"},
    )

    consumption = MealConsumption.objects.get(planned_meal=meal)
    assert response.status_code == 302
    assert consumption.status == MealConsumption.Status.COOKED
    assert PantryItem.objects.get(owner=user, name="Pasta", unit="g").quantity == Decimal("250.00")
    assert PantryItem.objects.get(owner=user, name="Tomato sauce", unit="unit").quantity == Decimal("1.00")
    assert PantryConsumptionEntry.objects.filter(consumption=consumption).count() == 2


@pytest.mark.django_db
def test_cooked_meal_never_makes_pantry_stock_negative_and_undo_restores_exact_deduction(client, django_user_model):
    user = django_user_model.objects.create_user(username="limited-stock", password="test-pass-123")
    meal = create_planned_meal(user)
    PantryItem.objects.create(owner=user, name="Pasta", quantity="100", unit="g")
    client.force_login(user)

    client.post(reverse("planner_outcome", kwargs={"pk": meal.pk}), {"action": "cooked"})

    assert not PantryItem.objects.filter(owner=user, name="Pasta", unit="g").exists()
    entry = PantryConsumptionEntry.objects.get(consumption__planned_meal=meal, name="Pasta")
    assert entry.quantity == Decimal("100.00")

    response = client.post(reverse("planner_outcome", kwargs={"pk": meal.pk}), {"action": "undo"})

    assert response.status_code == 302
    assert not MealConsumption.objects.filter(planned_meal=meal).exists()
    assert PantryItem.objects.get(owner=user, name="Pasta", unit="g").quantity == Decimal("100.00")


@pytest.mark.django_db
@pytest.mark.parametrize("action", ["skipped", "postponed"])
def test_non_cooked_meal_outcomes_do_not_deduct_pantry(client, django_user_model, action):
    user = django_user_model.objects.create_user(username=f"{action}-meal", password="test-pass-123")
    meal = create_planned_meal(user)
    PantryItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g")
    client.force_login(user)

    response = client.post(reverse("planner_outcome", kwargs={"pk": meal.pk}), {"action": action})

    consumption = MealConsumption.objects.get(planned_meal=meal)
    assert response.status_code == 302
    assert consumption.status == action
    assert PantryItem.objects.get(owner=user, name="Pasta", unit="g").quantity == Decimal("500.00")
    assert not PantryConsumptionEntry.objects.filter(consumption=consumption).exists()


@pytest.mark.django_db
def test_user_cannot_change_another_users_meal_outcome(client, django_user_model):
    owner = django_user_model.objects.create_user(username="meal-owner", password="test-pass-123")
    other_user = django_user_model.objects.create_user(username="meal-other", password="test-pass-123")
    meal = create_planned_meal(owner)
    client.force_login(other_user)

    response = client.post(reverse("planner_outcome", kwargs={"pk": meal.pk}), {"action": "cooked"})

    assert response.status_code == 404
    assert not MealConsumption.objects.filter(planned_meal=meal).exists()


@pytest.mark.django_db
def test_lunch_is_prompted_only_after_its_scheduled_time(django_user_model):
    user = django_user_model.objects.create_user(username="due-meal", password="test-pass-123")
    meal = create_planned_meal(user, meal_type=PlannedMeal.MealType.LUNCH)
    paris = ZoneInfo("Europe/Paris")

    assert is_planned_meal_due(meal, now=datetime(2026, 5, 25, 11, 59, tzinfo=paris)) is False
    assert is_planned_meal_due(meal, now=datetime(2026, 5, 25, 12, 0, tzinfo=paris)) is True


@pytest.mark.django_db
def test_planner_shows_due_meal_confirmation_actions(client, django_user_model):
    user = django_user_model.objects.create_user(username="due-meal-ui", password="test-pass-123")
    create_planned_meal(user, date="2026-05-24", meal_type=PlannedMeal.MealType.DINNER)
    client.force_login(user)

    response = client.get(reverse("planner"), {"week": "2026-05-18", "day": "2026-05-24"})

    content = response.content.decode()
    assert response.status_code == 200
    assert "Was this meal cooked?" in content
    assert "Yes, cooked" in content
    assert "Skipped" in content
    assert "Postpone" in content
