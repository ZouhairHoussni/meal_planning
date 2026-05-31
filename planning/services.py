from collections import defaultdict
from decimal import Decimal

from django.db import transaction

from pantry.models import PantryItem
from pantry.services import _add_pantry_quantity

from .models import MealConsumption, PantryConsumptionEntry


def _as_decimal(value):
    return Decimal(str(value or "0"))


def _restore_consumption_entries(consumption):
    for entry in consumption.entries.all():
        _add_pantry_quantity(
            consumption.planned_meal.owner,
            entry.name,
            entry.unit,
            _as_decimal(entry.quantity),
        )
    consumption.entries.all().delete()


def _deduct_recipe_components(consumption):
    component_totals = defaultdict(Decimal)
    display_names = {}
    for component in consumption.planned_meal.recipe.components.all():
        name = component.name.strip()
        key = (name.casefold(), component.unit)
        component_totals[key] += _as_decimal(component.quantity)
        display_names[key] = name

    for (normalized_name, unit), required_quantity in component_totals.items():
        if not normalized_name or required_quantity <= 0:
            continue
        item = (
            PantryItem.objects.select_for_update()
            .filter(
                owner=consumption.planned_meal.owner,
                name__iexact=display_names[(normalized_name, unit)],
                unit=unit,
            )
            .order_by("id")
            .first()
        )
        if item is None:
            continue

        deducted_quantity = min(_as_decimal(item.quantity), required_quantity)
        item.quantity = _as_decimal(item.quantity) - deducted_quantity
        if item.quantity <= 0:
            item.delete()
        else:
            item.save(update_fields=["quantity", "updated_at"])
        PantryConsumptionEntry.objects.create(
            consumption=consumption,
            name=item.name,
            quantity=deducted_quantity,
            unit=unit,
        )


@transaction.atomic
def set_meal_outcome(meal, action):
    if action == "undo":
        consumption = (
            MealConsumption.objects.select_for_update()
            .filter(planned_meal=meal)
            .select_related("planned_meal__owner")
            .first()
        )
        if consumption is None:
            return None
        _restore_consumption_entries(consumption)
        consumption.delete()
        return None

    valid_statuses = {
        MealConsumption.Status.COOKED,
        MealConsumption.Status.SKIPPED,
        MealConsumption.Status.POSTPONED,
    }
    if action not in valid_statuses:
        raise ValueError("Unsupported meal outcome")

    consumption, _ = MealConsumption.objects.select_for_update().get_or_create(
        planned_meal=meal,
        defaults={"status": action},
    )
    _restore_consumption_entries(consumption)
    consumption.status = action
    consumption.save(update_fields=["status", "decided_at"])

    if action == MealConsumption.Status.COOKED:
        _deduct_recipe_components(consumption)
    return consumption
