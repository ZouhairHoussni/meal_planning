from decimal import Decimal

import pytest
from django.urls import reverse

from planning.models import PlannedMeal
from recipes.models import Recipe, RecipeComponent
from shopping.models import ShoppingItem
from households.models import Household


@pytest.mark.django_db
def test_dashboard_shows_insights_for_meals_components_and_stores(client, django_user_model):
    user = django_user_model.objects.create_user(username="insight-user", password="test-pass-123")
    Household.objects.create(owner=user, name="Insight home", default_weekly_budget="80.00")
    pasta = Recipe.objects.create(owner=user, name="Pasta pesto")
    soup = Recipe.objects.create(owner=user, name="Soup")
    RecipeComponent.objects.create(recipe=pasta, name="Pasta", quantity="250", unit="g", brand="Barilla", store="Carrefour")
    RecipeComponent.objects.create(recipe=pasta, name="Pesto", quantity="40", unit="g", brand="Sacla", store="Carrefour")
    RecipeComponent.objects.create(recipe=soup, name="Carrot", quantity="300", unit="g", store="Market")
    PlannedMeal.objects.create(owner=user, recipe=pasta, date="2026-05-25", meal_type=PlannedMeal.MealType.DINNER)
    PlannedMeal.objects.create(owner=user, recipe=pasta, date="2026-05-26", meal_type=PlannedMeal.MealType.LUNCH)
    PlannedMeal.objects.create(owner=user, recipe=soup, date="2026-05-27", meal_type=PlannedMeal.MealType.DINNER)
    ShoppingItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g", price="2.50", store="Carrefour")
    ShoppingItem.objects.create(owner=user, name="Carrot", quantity="300", unit="g", price="1.25", store="Market")
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Most planned meal" in content
    assert "Pasta pesto" in content
    assert "Top components" in content
    assert "Pasta" in content
    assert "Spend by store" in content
    assert "Carrefour" in content
    assert "EUR 2.50" in content


@pytest.mark.django_db
def test_dashboard_store_filter_limits_shopping_summary(client, django_user_model):
    user = django_user_model.objects.create_user(username="filter-user", password="test-pass-123")
    Household.objects.create(owner=user, name="Filter home", default_weekly_budget="80.00")
    ShoppingItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g", price="2.50", store="Carrefour")
    ShoppingItem.objects.create(owner=user, name="Carrot", quantity="300", unit="g", price="1.25", store="Market")
    client.force_login(user)

    response = client.get(reverse("dashboard"), {"store": "Market"})

    content = response.content.decode()
    assert response.status_code == 200
    assert "EUR 1.25" in content
    assert "Market" in content


@pytest.mark.django_db
def test_dashboard_insight_selector_returns_store_totals(django_user_model):
    from core.selectors import dashboard_insights_for_user

    user = django_user_model.objects.create_user(username="selector-user", password="test-pass-123")
    ShoppingItem.objects.create(owner=user, name="A", quantity="1", unit="unit", price="2.00", store="Store A")
    ShoppingItem.objects.create(owner=user, name="B", quantity="1", unit="unit", price="3.00", store="Store A")
    ShoppingItem.objects.create(owner=user, name="C", quantity="1", unit="unit", price="1.50", store="Store B")

    insights = dashboard_insights_for_user(user)

    assert insights.store_totals[0].store == "Store A"
    assert insights.store_totals[0].total == Decimal("5.00")

    filtered = dashboard_insights_for_user(user, store="Store B")
    assert len(filtered.store_totals) == 1
    assert filtered.store_totals[0].store == "Store B"
    assert filtered.store_totals[0].total == Decimal("1.50")
