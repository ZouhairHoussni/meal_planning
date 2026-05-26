from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from recipes.models import Recipe
from shopping.services import sync_planned_shopping_items

from .forms import PlannedMealForm
from .models import PlannedMeal


def monday_for(value):
    return value - timedelta(days=value.weekday())


@login_required
def planner(request):
    selected = parse_date(request.GET.get("week", "")) or date.today()
    week_start = monday_for(selected)
    days = [week_start + timedelta(days=offset) for offset in range(7)]
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
    return redirect("planner")


@login_required
def planner_delete(request, pk):
    meal = get_object_or_404(PlannedMeal, pk=pk, owner=request.user)
    if request.method == "POST":
        meal.delete()
        sync_planned_shopping_items(request.user)
    return redirect("planner")
