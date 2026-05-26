from collections import defaultdict
from decimal import Decimal

from planning.models import PlannedMeal

from .models import ShoppingItem


def sync_planned_shopping_items(user):
    totals = defaultdict(Decimal)
    display_values = {}
    for meal in (
        PlannedMeal.objects.filter(owner=user)
        .select_related("recipe")
        .prefetch_related("recipe__components")
    ):
        for component in meal.recipe.components.all():
            brand = component.brand or ""
            store = component.store or ""
            key = (component.name.strip().casefold(), component.unit, brand.casefold(), store.casefold())
            totals[key] += component.quantity
            display_values[key] = {
                "name": component.name.strip(),
                "brand": brand,
                "store": store,
            }

    seen_keys = set(totals.keys())
    for item in ShoppingItem.objects.filter(owner=user, source=ShoppingItem.Source.PLANNED):
        key = (item.name.strip().casefold(), item.unit, (item.brand or "").casefold(), (item.store or "").casefold())
        if key not in seen_keys:
            item.delete()

    for (normalized_name, unit, normalized_brand, normalized_store), quantity in totals.items():
        if not normalized_name:
            continue
        values = display_values[(normalized_name, unit, normalized_brand, normalized_store)]
        item = (
            ShoppingItem.objects.filter(
                owner=user,
                source=ShoppingItem.Source.PLANNED,
                unit=unit,
                name__iexact=values["name"],
                brand=values["brand"],
                store=values["store"],
            )
            .order_by("id")
            .first()
        )
        if item:
            item.name = values["name"]
            item.quantity = quantity
            item.save(update_fields=["name", "quantity", "updated_at"])
        else:
            ShoppingItem.objects.create(
                owner=user,
                name=values["name"],
                quantity=quantity,
                unit=unit,
                source=ShoppingItem.Source.PLANNED,
                brand=values["brand"],
                store=values["store"],
            )
