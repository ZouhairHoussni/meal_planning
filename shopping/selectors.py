from dataclasses import dataclass
from decimal import Decimal

from .models import ShoppingItem


@dataclass(frozen=True)
class ShoppingSummary:
    total_price: Decimal
    item_count: int
    priced_count: int
    missing_price_count: int
    purchased_count: int


def shopping_items_for_user(user, store=None, source=None):
    items = ShoppingItem.objects.filter(owner=user)
    if store:
        items = items.filter(store=store)
    if source in {ShoppingItem.Source.PLANNED, ShoppingItem.Source.MANUAL}:
        items = items.filter(source=source)
    return items


def shopping_summary_for_user(user, store=None, source=None):
    items = shopping_items_for_user(user, store=store, source=source)
    total = Decimal("0.00")
    item_count = 0
    priced_count = 0
    missing_price_count = 0
    purchased_count = 0

    for item in items:
        item_count += 1
        if item.purchased:
            purchased_count += 1
        if item.price is None:
            missing_price_count += 1
        else:
            priced_count += 1
            total += item.price

    return ShoppingSummary(
        total_price=total,
        item_count=item_count,
        priced_count=priced_count,
        missing_price_count=missing_price_count,
        purchased_count=purchased_count,
    )
