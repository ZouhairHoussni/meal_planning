from decimal import Decimal

import pytest

from shopping.models import ShoppingItem
from shopping.selectors import shopping_summary_for_user


@pytest.mark.django_db
def test_shopping_summary_totals_priced_items_and_counts_missing_prices(django_user_model):
    user = django_user_model.objects.create_user(username="summary-user", password="test-pass-123")
    ShoppingItem.objects.create(owner=user, name="Eggs", quantity="6", unit="unit", price="2.80")
    ShoppingItem.objects.create(owner=user, name="Coffee", quantity="1", unit="unit", price="4.50")
    ShoppingItem.objects.create(owner=user, name="Rice", quantity="500", unit="g")

    summary = shopping_summary_for_user(user)

    assert summary.total_price == Decimal("7.30")
    assert summary.item_count == 3
    assert summary.priced_count == 2
    assert summary.missing_price_count == 1
