import pytest
from django.urls import reverse

from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_shopping_page_uses_phone_first_shop_mode_sections(client, django_user_model):
    user = django_user_model.objects.create_user(username="shop-mode-user", password="test-pass-123")
    ShoppingItem.objects.create(owner=user, name="Milk", quantity="1", unit="l", store="Carrefour", price="1.20")
    ShoppingItem.objects.create(owner=user, name="Bread", quantity="1", unit="unit", purchased=True, price="1.80")
    client.force_login(user)

    response = client.get(reverse("shopping"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Shop mode" in content
    assert "Quick add" in content
    assert 'data-shopping-quick-add-panel' in content
    assert 'data-shopping-quick-add-toggle' in content
    assert "hidden md:block" in content
    assert "Still to buy" in content
    assert "Already in pantry" in content
    assert "Edit item details" in content
    assert "aria-label=\"Mark Milk as bought\"" in content
