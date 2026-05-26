from decimal import Decimal

import pytest
from django.urls import reverse

from recipes.models import Recipe, RecipeComponent


@pytest.mark.django_db
def test_user_can_create_recipe_with_components(client, django_user_model):
    user = django_user_model.objects.create_user(username="recipe-user", password="test-pass-123")
    client.force_login(user)

    response = client.post(
        reverse("recipe_new"),
        {
            "name": "Pasta night",
            "description": "Fast dinner",
            "components-TOTAL_FORMS": "2",
            "components-INITIAL_FORMS": "0",
            "components-MIN_NUM_FORMS": "0",
            "components-MAX_NUM_FORMS": "1000",
            "components-0-name": "Pasta",
            "components-0-quantity": "500",
            "components-0-unit": "g",
            "components-0-brand": "Barilla",
            "components-0-store": "Carrefour",
            "components-0-note": "",
            "components-1-name": "Tomato sauce",
            "components-1-quantity": "300",
            "components-1-unit": "g",
            "components-1-brand": "",
            "components-1-store": "",
            "components-1-note": "",
        },
    )

    recipe = Recipe.objects.get(owner=user, name="Pasta night")
    assert response.status_code == 302
    assert response["Location"] == recipe.get_absolute_url()
    assert RecipeComponent.objects.filter(recipe=recipe).count() == 2
    assert recipe.components.get(name="Pasta").quantity == Decimal("500")
    assert recipe.components.get(name="Pasta").brand == "Barilla"
    assert recipe.components.get(name="Pasta").store == "Carrefour"


@pytest.mark.django_db
def test_recipe_form_uses_meal_language_and_has_add_component_control(client, django_user_model):
    user = django_user_model.objects.create_user(username="meal-form-user", password="test-pass-123")
    client.force_login(user)

    response = client.get(reverse("recipe_new"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Create meal" in content
    assert "Add component" in content


@pytest.mark.django_db
def test_user_can_edit_recipe_and_component_brand_store(client, django_user_model):
    user = django_user_model.objects.create_user(username="edit-recipe-user", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    component = RecipeComponent.objects.create(recipe=recipe, name="Pasta", quantity="250", unit="g")
    client.force_login(user)

    response = client.post(
        reverse("recipe_edit", kwargs={"pk": recipe.pk}),
        {
            "name": "Pasta pesto",
            "description": "Fast",
            "components-TOTAL_FORMS": "1",
            "components-INITIAL_FORMS": "1",
            "components-MIN_NUM_FORMS": "0",
            "components-MAX_NUM_FORMS": "1000",
            "components-0-id": str(component.id),
            "components-0-name": "Pasta",
            "components-0-quantity": "300",
            "components-0-unit": "g",
            "components-0-brand": "Barilla",
            "components-0-store": "Carrefour",
            "components-0-note": "whole wheat",
        },
    )

    recipe.refresh_from_db()
    component.refresh_from_db()
    assert response.status_code == 302
    assert recipe.name == "Pasta pesto"
    assert component.quantity == Decimal("300")
    assert component.brand == "Barilla"
    assert component.store == "Carrefour"
