from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import HouseholdForm
from .selectors import household_for_user


@login_required
def onboarding(request):
    existing_household = household_for_user(request.user)
    if existing_household:
        return redirect("dashboard")

    form = HouseholdForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        household = form.save(commit=False)
        household.owner = request.user
        household.currency = "EUR"
        household.save()
        return redirect("dashboard")

    return render(request, "households/onboarding.html", {"form": form})


@login_required
def settings(request):
    household = household_for_user(request.user)
    if not household:
        return redirect("household_onboarding")

    form = HouseholdForm(request.POST or None, instance=household)
    if request.method == "POST" and form.is_valid():
        household = form.save(commit=False)
        household.currency = "EUR"
        household.save()
        return redirect("dashboard")

    return render(request, "households/settings.html", {"form": form, "household": household})
