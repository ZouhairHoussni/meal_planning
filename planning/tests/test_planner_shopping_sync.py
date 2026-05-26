import pytest
from django.urls import reverse

from planning.models import PlannedMeal
from recipes.models import Recipe, RecipeComponent
from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_adding_recipe_to_planner_syncs_recipe_components_to_shopping(client, django_user_model):
    user = django_user_model.objects.create_user(username="planner-user", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Omelette")
    RecipeComponent.objects.create(recipe=recipe, name="Eggs", quantity="6", unit="unit")
    RecipeComponent.objects.create(recipe=recipe, name="Potatoes", quantity="500", unit="g")
    client.force_login(user)

    response = client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-25",
            "meal_type": PlannedMeal.MealType.BREAKFAST,
        },
    )

    assert response.status_code == 302
    assert PlannedMeal.objects.filter(owner=user, recipe=recipe, meal_type=PlannedMeal.MealType.BREAKFAST).exists()
    assert ShoppingItem.objects.filter(owner=user, source=ShoppingItem.Source.PLANNED, name="Eggs", quantity="6").exists()
    assert ShoppingItem.objects.filter(owner=user, source=ShoppingItem.Source.PLANNED, name="Potatoes", quantity="500").exists()


@pytest.mark.django_db
def test_planner_sync_creates_planned_shopping_items_with_empty_optional_metadata(client, django_user_model):
    user = django_user_model.objects.create_user(username="metadata-sync", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    RecipeComponent.objects.create(recipe=recipe, name="Pasta", quantity="250", unit="g")
    client.force_login(user)

    response = client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-25",
            "meal_type": PlannedMeal.MealType.DINNER,
        },
    )

    item = ShoppingItem.objects.get(owner=user, source=ShoppingItem.Source.PLANNED, name="Pasta")
    assert response.status_code == 302
    assert item.brand == ""
    assert item.store == ""


@pytest.mark.django_db
def test_planner_sync_carries_component_brand_and_store_to_shopping(client, django_user_model):
    user = django_user_model.objects.create_user(username="component-store-sync", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    RecipeComponent.objects.create(
        recipe=recipe,
        name="Pasta",
        quantity="250",
        unit="g",
        brand="Barilla",
        store="Carrefour",
    )
    client.force_login(user)

    response = client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-25",
            "meal_type": PlannedMeal.MealType.DINNER,
        },
    )

    item = ShoppingItem.objects.get(owner=user, source=ShoppingItem.Source.PLANNED, name="Pasta")
    assert response.status_code == 302
    assert item.brand == "Barilla"
    assert item.store == "Carrefour"


@pytest.mark.django_db
def test_deleting_planned_meal_resyncs_shopping_without_optional_metadata_crash(client, django_user_model):
    user = django_user_model.objects.create_user(username="delete-sync", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    RecipeComponent.objects.create(recipe=recipe, name="Pasta", quantity="250", unit="g")
    meal = PlannedMeal.objects.create(
        owner=user,
        recipe=recipe,
        date="2026-05-25",
        meal_type=PlannedMeal.MealType.DINNER,
    )
    client.force_login(user)

    response = client.post(reverse("planner_delete", kwargs={"pk": meal.pk}))

    assert response.status_code == 302
    assert not PlannedMeal.objects.filter(pk=meal.pk).exists()
    assert not ShoppingItem.objects.filter(owner=user, source=ShoppingItem.Source.PLANNED, name="Pasta").exists()


@pytest.mark.django_db
def test_adding_same_recipe_to_same_slot_twice_does_not_crash_or_duplicate(client, django_user_model):
    user = django_user_model.objects.create_user(username="duplicate-planner", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Pasta")
    RecipeComponent.objects.create(recipe=recipe, name="Pasta", quantity="500", unit="g")
    client.force_login(user)
    payload = {
        "recipe": recipe.id,
        "date": "2026-05-25",
        "meal_type": PlannedMeal.MealType.DINNER,
    }

    first_response = client.post(reverse("planner_add"), payload)
    second_response = client.post(reverse("planner_add"), payload)

    assert first_response.status_code == 302
    assert second_response.status_code == 302
    assert PlannedMeal.objects.filter(
        owner=user,
        recipe=recipe,
        date="2026-05-25",
        meal_type=PlannedMeal.MealType.DINNER,
    ).count() == 1
    assert ShoppingItem.objects.filter(owner=user, source=ShoppingItem.Source.PLANNED, name="Pasta").count() == 1


@pytest.mark.django_db
def test_manual_shopping_item_is_kept_when_planned_items_sync(client, django_user_model):
    user = django_user_model.objects.create_user(username="shopper", password="test-pass-123")
    recipe = Recipe.objects.create(owner=user, name="Soup")
    RecipeComponent.objects.create(recipe=recipe, name="Carrots", quantity="300", unit="g")
    ShoppingItem.objects.create(owner=user, name="Chocolate", quantity="1", unit="unit", source=ShoppingItem.Source.MANUAL)
    client.force_login(user)

    client.post(
        reverse("planner_add"),
        {
            "recipe": recipe.id,
            "date": "2026-05-25",
            "meal_type": PlannedMeal.MealType.DINNER,
        },
    )

    assert ShoppingItem.objects.filter(owner=user, name="Carrots", source=ShoppingItem.Source.PLANNED).exists()
    assert ShoppingItem.objects.filter(owner=user, name="Chocolate", source=ShoppingItem.Source.MANUAL).exists()


@pytest.mark.django_db
def test_user_can_add_manual_grocery_item(client, django_user_model):
    user = django_user_model.objects.create_user(username="manual-shopper", password="test-pass-123")
    client.force_login(user)

    response = client.post(
        reverse("shopping_add_manual"),
        {
            "name": "Coffee",
            "quantity": "1",
            "unit": "unit",
        },
    )

    assert response.status_code == 302
    assert ShoppingItem.objects.filter(owner=user, name="Coffee", source=ShoppingItem.Source.MANUAL).exists()
