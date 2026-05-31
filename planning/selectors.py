from datetime import datetime, time

from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import PlannedMeal


MEAL_TIMES = {
    PlannedMeal.MealType.BREAKFAST: time(hour=8),
    PlannedMeal.MealType.LUNCH: time(hour=12),
    PlannedMeal.MealType.DINNER: time(hour=19),
    PlannedMeal.MealType.EXTRA: time(hour=0),
}


def is_planned_meal_due(meal, *, now=None):
    current_time = now or timezone.now()
    if timezone.is_naive(current_time):
        current_time = timezone.make_aware(current_time)
    current_time = timezone.localtime(current_time)
    meal_date = parse_date(meal.date) if isinstance(meal.date, str) else meal.date
    meal_time = datetime.combine(
        meal_date,
        MEAL_TIMES[meal.meal_type],
        tzinfo=timezone.get_current_timezone(),
    )
    return current_time >= meal_time
