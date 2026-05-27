import pytest
from django.urls import reverse

from planning.models import PlannedMeal
from recipes.models import Recipe


@pytest.mark.django_db
def test_planner_uses_slot_first_mobile_layout(client, django_user_model):
    user = django_user_model.objects.create_user(username="planner-ui", password="test-pass-123")
    Recipe.objects.create(owner=user, name="Pasta")
    client.force_login(user)

    response = client.get(reverse("planner"), {"week": "2026-05-25", "day": "2026-05-26"})

    content = response.content.decode()
    assert response.status_code == 200
    assert "Meal Planner" in content
    assert "25-31 May" in content
    assert 'data-planner-day-tab="2026-05-26"' in content
    assert 'data-planner-day-panel="2026-05-26"' in content
    assert 'data-planner-add-trigger' in content
    assert "+ Add dinner" in content
    assert 'data-planner-sheet' in content
    assert "Add meal to slot" in content


@pytest.mark.django_db
def test_planner_add_redirects_to_safe_next_url(client, django_user_model):
    user = django_user_model.objects.create_user(username="planner-next", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Soup")
    client.force_login(user)

    response = client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-26",
            "meal_type": PlannedMeal.MealType.DINNER,
            "next": "/planner/?week=2026-05-25&day=2026-05-26",
        },
    )

    assert response.status_code == 302
    assert response.url == "/planner/?week=2026-05-25&day=2026-05-26"


@pytest.mark.django_db
def test_planner_add_ignores_unsafe_next_url(client, django_user_model):
    user = django_user_model.objects.create_user(username="planner-unsafe-next", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Soup")
    client.force_login(user)

    response = client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-26",
            "meal_type": PlannedMeal.MealType.LUNCH,
            "next": "https://example.com/not-this-app",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("planner")
