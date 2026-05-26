import pytest
from django.urls import reverse

from households.models import Household


@pytest.mark.django_db
@pytest.mark.parametrize(
    "route_name, expected_text",
    [
        ("recipe_list", "Recipe library"),
        ("planner", "Drag recipes"),
        ("shopping", "Shopping list"),
        ("pantry", "What you have at home"),
    ],
)
def test_authenticated_primary_pages_render(client, django_user_model, route_name, expected_text):
    user = django_user_model.objects.create_user(username=f"{route_name}-user", password="test-pass-123")
    client.force_login(user)

    response = client.get(reverse(route_name))

    assert response.status_code == 200
    assert expected_text in response.content.decode()


@pytest.mark.django_db
def test_admin_branding_uses_mealbudget_name(client, django_user_model):
    admin = django_user_model.objects.create_superuser(
        username="admin-smoke",
        email="admin@example.com",
        password="test-pass-123",
    )
    client.force_login(admin)

    response = client.get(reverse("admin:index"))

    assert response.status_code == 200
    assert "MealBudget admin" in response.content.decode()


@pytest.mark.django_db
def test_dashboard_shows_meal_and_shopping_summary(client, django_user_model):
    from planning.models import PlannedMeal
    from recipes.models import Recipe
    from shopping.models import ShoppingItem

    user = django_user_model.objects.create_user(username="dashboard-summary", password="test-pass-123")
    Household.objects.create(owner=user, name="Summary home", default_weekly_budget="80.00")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    PlannedMeal.objects.create(owner=user, recipe=recipe, date="2026-05-25", meal_type=PlannedMeal.MealType.DINNER)
    ShoppingItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g", price="1.50")
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "EUR 1.50" in content
    assert "1 meal planned" in content
