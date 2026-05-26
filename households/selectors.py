from dataclasses import dataclass
from decimal import Decimal

from shopping.selectors import shopping_summary_for_user

from .models import Household


@dataclass(frozen=True)
class BudgetStatus:
    budget: Decimal
    known_spend: Decimal
    remaining: Decimal
    display_delta: Decimal
    is_over_budget: bool
    percentage: int
    bar_percentage: int


def household_for_user(user):
    return Household.objects.filter(owner=user).first()


def budget_status_for_user(user, household):
    summary = shopping_summary_for_user(user)
    budget = Decimal(str(household.default_weekly_budget))
    remaining = budget - summary.total_price
    percentage = 0
    if budget > 0:
        percentage = min(int((summary.total_price / budget) * 100), 999)
    return BudgetStatus(
        budget=budget,
        known_spend=summary.total_price,
        remaining=remaining,
        display_delta=abs(remaining),
        is_over_budget=remaining < 0,
        percentage=percentage,
        bar_percentage=min(percentage, 100),
    )
