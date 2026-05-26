from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Count

from planning.models import PlannedMeal
from shopping.models import ShoppingItem
from shopping.selectors import shopping_items_for_user, shopping_summary_for_user


@dataclass(frozen=True)
class MealInsight:
    name: str
    count: int


@dataclass(frozen=True)
class ComponentInsight:
    name: str
    unit: str
    quantity: Decimal
    brand: str
    store: str


@dataclass(frozen=True)
class StoreTotal:
    store: str
    total: Decimal
    item_count: int


@dataclass(frozen=True)
class DashboardInsights:
    active_store: str
    active_source: str
    available_stores: list[str]
    shopping_summary: object
    most_planned_meal: MealInsight | None
    top_components: list[ComponentInsight]
    store_totals: list[StoreTotal]


def dashboard_insights_for_user(user, store="", source=""):
    store = store or ""
    source = source or ""
    store_filter = store or None
    source_filter = source or None

    meal_row = (
        PlannedMeal.objects.filter(owner=user)
        .values("recipe__name")
        .annotate(count=Count("id"))
        .order_by("-count", "recipe__name")
        .first()
    )
    most_planned_meal = None
    if meal_row:
        most_planned_meal = MealInsight(name=meal_row["recipe__name"], count=meal_row["count"])

    component_totals = defaultdict(lambda: Decimal("0.00"))
    component_display = {}
    meals = (
        PlannedMeal.objects.filter(owner=user)
        .select_related("recipe")
        .prefetch_related("recipe__components")
    )
    for meal in meals:
        for component in meal.recipe.components.all():
            key = (
                component.name.strip().casefold(),
                component.unit,
                (component.brand or "").casefold(),
                (component.store or "").casefold(),
            )
            component_totals[key] += component.quantity
            component_display[key] = component

    top_components = []
    for key, quantity in sorted(component_totals.items(), key=lambda item: item[1], reverse=True)[:5]:
        component = component_display[key]
        top_components.append(
            ComponentInsight(
                name=component.name,
                unit=component.unit,
                quantity=quantity,
                brand=component.brand or "",
                store=component.store or "",
            )
        )

    store_map = defaultdict(lambda: {"total": Decimal("0.00"), "count": 0})
    for item in shopping_items_for_user(user, store=store_filter, source=source_filter):
        label = item.store or "No store yet"
        store_map[label]["count"] += 1
        if item.price is not None:
            store_map[label]["total"] += item.price

    store_totals = [
        StoreTotal(store=label, total=data["total"], item_count=data["count"])
        for label, data in store_map.items()
    ]
    store_totals.sort(key=lambda row: row.total, reverse=True)

    available_stores = sorted(
        store
        for store in ShoppingItem.objects.filter(owner=user)
        .exclude(store__isnull=True)
        .exclude(store="")
        .values_list("store", flat=True)
        .distinct()
    )

    return DashboardInsights(
        active_store=store,
        active_source=source,
        available_stores=available_stores,
        shopping_summary=shopping_summary_for_user(user, store=store_filter, source=source_filter),
        most_planned_meal=most_planned_meal,
        top_components=top_components,
        store_totals=store_totals,
    )
