from decimal import Decimal

from django.db import transaction

from .models import PantryItem


def _as_decimal(value):
    return Decimal(str(value or "0"))


def _find_pantry_item(owner, name, unit):
    return PantryItem.objects.filter(owner=owner, unit=unit, name__iexact=name).order_by("id").first()


def _add_pantry_quantity(owner, name, unit, quantity):
    if quantity <= 0:
        return
    item = _find_pantry_item(owner, name, unit)
    if item is None:
        PantryItem.objects.create(owner=owner, name=name, unit=unit, quantity=quantity)
        return
    item.quantity = _as_decimal(item.quantity) + quantity
    item.save(update_fields=["quantity", "updated_at"])


def _subtract_pantry_quantity(owner, name, unit, quantity):
    if quantity <= 0:
        return
    item = _find_pantry_item(owner, name, unit)
    if item is None:
        return
    item.quantity = _as_decimal(item.quantity) - quantity
    if item.quantity <= 0:
        item.delete()
    else:
        item.save(update_fields=["quantity", "updated_at"])


@transaction.atomic
def sync_shopping_item_to_pantry(item):
    synced_quantity = _as_decimal(item.pantry_synced_quantity)
    synced_name = (item.pantry_synced_name or "").strip()
    synced_unit = item.pantry_synced_unit or ""

    if synced_quantity > 0 and synced_name and synced_unit:
        _subtract_pantry_quantity(item.owner, synced_name, synced_unit, synced_quantity)

    item.pantry_synced_quantity = Decimal("0.00")
    item.pantry_synced_name = ""
    item.pantry_synced_unit = ""

    if item.purchased:
        item_name = item.name.strip()
        item_quantity = _as_decimal(item.quantity)
        if item_name and item_quantity > 0:
            _add_pantry_quantity(item.owner, item_name, item.unit, item_quantity)
            item.pantry_synced_quantity = item_quantity
            item.pantry_synced_name = item_name
            item.pantry_synced_unit = item.unit

    item.save(
        update_fields=[
            "pantry_synced_quantity",
            "pantry_synced_name",
            "pantry_synced_unit",
            "updated_at",
        ]
    )
