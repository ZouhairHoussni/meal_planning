from decimal import Decimal

import pytest
from django.urls import reverse

from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_manual_grocery_item_can_store_price_brand_and_store(client, django_user_model):
    user = django_user_model.objects.create_user(username="priced-shopper", password="test-pass-123")
    client.force_login(user)

    response = client.post(
        reverse("shopping_add_manual"),
        {
            "name": "Coffee",
            "quantity": "1",
            "unit": "unit",
            "price": "4.50",
            "brand": "Lavazza",
            "store": "Carrefour",
        },
    )

    item = ShoppingItem.objects.get(owner=user, name="Coffee")
    assert response.status_code == 302
    assert item.price == Decimal("4.50")
    assert item.brand == "Lavazza"
    assert item.store == "Carrefour"


@pytest.mark.django_db
def test_existing_grocery_item_can_be_updated_with_price_brand_and_store(client, django_user_model):
    user = django_user_model.objects.create_user(username="planned-price", password="test-pass-123")
    item = ShoppingItem.objects.create(
        owner=user,
        name="Eggs",
        quantity="6",
        unit="unit",
        source=ShoppingItem.Source.PLANNED,
    )
    client.force_login(user)

    response = client.post(
        reverse("shopping_update", kwargs={"pk": item.pk}),
        {
            "name": "Eggs",
            "quantity": "6",
            "unit": "unit",
            "price": "2.80",
            "brand": "Local farm",
            "store": "Market",
        },
    )

    item.refresh_from_db()
    assert response.status_code == 302
    assert item.price == Decimal("2.80")
    assert item.brand == "Local farm"
    assert item.store == "Market"


@pytest.mark.django_db
def test_shopping_page_shows_total_price(client, django_user_model):
    user = django_user_model.objects.create_user(username="priced-page", password="test-pass-123")
    ShoppingItem.objects.create(owner=user, name="Milk", quantity="1", unit="l", price="1.20")
    ShoppingItem.objects.create(owner=user, name="Bread", quantity="1", unit="unit", price="1.80")
    client.force_login(user)

    response = client.get(reverse("shopping"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "EUR 3.00" in content
    assert "2 priced" in content
