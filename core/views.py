from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.selectors import dashboard_insights_for_user
from planning.models import PlannedMeal


def home(request):
    return redirect("dashboard")


@login_required
def dashboard(request):
    meal_count = PlannedMeal.objects.filter(owner=request.user).count()
    insights = dashboard_insights_for_user(
        request.user,
        store=request.GET.get("store", ""),
        source=request.GET.get("source", ""),
    )
    return render(
        request,
        "core/dashboard.html",
        {
            "meal_count": meal_count,
            "shopping_summary": insights.shopping_summary,
            "insights": insights,
        },
    )
