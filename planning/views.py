from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from django.utils.http import url_has_allowed_host_and_scheme

from recipes.models import Recipe
from shopping.services import sync_planned_shopping_items

from .forms import PlannedMealForm
from .models import PlannedMeal


def monday_for(value):
    return value - timedelta(days=value.weekday())


def format_week_range(week_start, week_end):
    if week_start.year == week_end.year and week_start.month == week_end.month:
        return f"{week_start.day}-{week_end.day} {week_end:%b}"
    if week_start.year == week_end.year:
        return f"{week_start.day} {week_start:%b} - {week_end.day} {week_end:%b}"
    return f"{week_start.day} {week_start:%b} {week_start.year} - {week_end.day} {week_end:%b} {week_end.year}"


def safe_next_url(request):
    target = request.POST.get("next") or request.GET.get("next")
    if target and url_has_allowed_host_and_scheme(
        target,
        allowed_hosts={request.get_host(), *settings.ALLOWED_HOSTS},
        require_https=request.is_secure(),
    ):
        return target
    return None


@login_required
def planner(request):
    selected = parse_date(request.GET.get("week", "")) or date.today()
    week_start = monday_for(selected)
    days = [week_start + timedelta(days=offset) for offset in range(7)]
    week_end = days[-1]
    requested_day = parse_date(request.GET.get("day", ""))
    today = date.today()
    selected_day = requested_day if requested_day in days else today if today in days else week_start
    meals = PlannedMeal.objects.filter(owner=request.user, date__range=(days[0], days[-1])).select_related("recipe")
    recipes = Recipe.objects.filter(owner=request.user).prefetch_related("components")
    meals_by_day = {day: {choice.value: [] for choice in PlannedMeal.MealType} for day in days}
    for meal in meals:
        meals_by_day[meal.date][meal.meal_type].append(meal)
    week_rows = [
        {
            "date": day,
            "slots": [
                {"type": choice.value, "label": choice.label, "meals": meals_by_day[day][choice.value]}
                for choice in PlannedMeal.MealType
            ],
        }
        for day in days
    ]

    return render(
        request,
        "planning/planner.html",
        {
            "days": days,
            "week_rows": week_rows,
            "week_start": week_start,
            "week_end": week_end,
            "week_label": format_week_range(week_start, week_end),
            "previous_week": week_start - timedelta(days=7),
            "next_week": week_start + timedelta(days=7),
            "selected_day": selected_day,
            "meal_types": PlannedMeal.MealType,
            "recipes": recipes,
            "form": PlannedMealForm(owner=request.user),
        },
    )


@login_required
def planner_add(request):
    if request.method != "POST":
        return redirect("planner")

    form = PlannedMealForm(request.POST, owner=request.user)
    if form.is_valid():
        cleaned = form.cleaned_data
        planned_meal, created = PlannedMeal.objects.get_or_create(
            owner=request.user,
            recipe=cleaned["recipe"],
            date=cleaned["date"],
            meal_type=cleaned["meal_type"],
            defaults={"note": cleaned.get("note", "")},
        )
        if not created and cleaned.get("note") and planned_meal.note != cleaned["note"]:
            planned_meal.note = cleaned["note"]
            planned_meal.save(update_fields=["note"])
        if not created:
            messages.info(request, "That meal is already in this slot.")
        sync_planned_shopping_items(request.user)
    return redirect(safe_next_url(request) or "planner")


@login_required
def planner_delete(request, pk):
    meal = get_object_or_404(PlannedMeal, pk=pk, owner=request.user)
    if request.method == "POST":
        meal.delete()
        sync_planned_shopping_items(request.user)
    return redirect(safe_next_url(request) or "planner")
