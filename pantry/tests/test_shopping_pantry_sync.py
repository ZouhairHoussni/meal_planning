from decimal import Decimal

import pytest
from django.urls import reverse

from pantry.models import PantryItem
from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_marking_shopping_item_purchased_adds_it_to_pantry(client, django_user_model):
    user = django_user_model.objects.create_user(username="pantry-sync", password="test-pass-123")
    item = ShoppingItem.objects.create(owner=user, name="Pasta", quantity="500", unit="g")
    client.force_login(user)

    response = client.post(reverse("shopping_toggle", kwargs={"pk": item.pk}))

    pantry_item = PantryItem.objects.get(owner=user, name="Pasta", unit="g")
    item.refresh_from_db()
    assert response.status_code == 302
    assert pantry_item.quantity == Decimal("500.00")
    assert item.purchased is True
    assert item.pantry_synced_quantity == Decimal("500.00")


@pytest.mark.django_db
def test_unmarking_purchased_item_reverses_its_pantry_contribution(client, django_user_model):
    user = django_user_model.objects.create_user(username="pantry-reverse", password="test-pass-123")
    PantryItem.objects.create(owner=user, name="Rice", quantity="10", unit="kg")
    item = ShoppingItem.objects.create(owner=user, name="Rice", quantity="2", unit="kg")
    client.force_login(user)

    client.post(reverse("shopping_toggle", kwargs={"pk": item.pk}))
    assert PantryItem.objects.get(owner=user, name="Rice", unit="kg").quantity == Decimal("12.00")

    response = client.post(reverse("shopping_toggle", kwargs={"pk": item.pk}))

    item.refresh_from_db()
    pantry_item = PantryItem.objects.get(owner=user, name="Rice", unit="kg")
    assert response.status_code == 302
    assert pantry_item.quantity == Decimal("10.00")
    assert item.purchased is False
    assert item.pantry_synced_quantity == Decimal("0.00")


@pytest.mark.django_db
def test_updating_purchased_item_resyncs_pantry_without_duplication(client, django_user_model):
    user = django_user_model.objects.create_user(username="pantry-update", password="test-pass-123")
    item = ShoppingItem.objects.create(owner=user, name="Coffee", quantity="1", unit="unit", purchased=False)
    client.force_login(user)
    client.post(reverse("shopping_toggle", kwargs={"pk": item.pk}))

    response = client.post(
        reverse("shopping_update", kwargs={"pk": item.pk}),
        {
            "name": "Coffee",
            "quantity": "3",
            "unit": "unit",
            "price": "12.50",
            "brand": "Lavazza",
            "store": "Carrefour",
        },
    )

    item.refresh_from_db()
    pantry_item = PantryItem.objects.get(owner=user, name="Coffee", unit="unit")
    assert response.status_code == 302
    assert pantry_item.quantity == Decimal("3.00")
    assert item.pantry_synced_quantity == Decimal("3.00")


@pytest.mark.django_db
def test_user_can_manually_adjust_pantry_quantity(client, django_user_model):
    user = django_user_model.objects.create_user(username="pantry-adjust", password="test-pass-123")
    item = PantryItem.objects.create(owner=user, name="Rice", quantity="2", unit="kg")
    client.force_login(user)

    response = client.post(
        reverse("pantry_update", kwargs={"pk": item.pk}),
        {
            "name": "Rice",
            "quantity": "1.25",
            "unit": "kg",
        },
    )

    item.refresh_from_db()
    assert response.status_code == 302
    assert item.quantity == Decimal("1.25")


@pytest.mark.django_db
def test_user_cannot_adjust_another_users_pantry_item(client, django_user_model):
    owner = django_user_model.objects.create_user(username="pantry-owner", password="test-pass-123")
    other_user = django_user_model.objects.create_user(username="pantry-other", password="test-pass-123")
    item = PantryItem.objects.create(owner=owner, name="Rice", quantity="2", unit="kg")
    client.force_login(other_user)

    response = client.post(
        reverse("pantry_update", kwargs={"pk": item.pk}),
        {
            "name": "Rice",
            "quantity": "1",
            "unit": "kg",
        },
    )

    assert response.status_code == 404
