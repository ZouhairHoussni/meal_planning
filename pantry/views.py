from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from planning.models import MealConsumption

from .forms import PantryItemForm
from .models import PantryItem


@login_required
def pantry(request):
    form = PantryItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        return redirect("pantry")

    return render(
        request,
        "pantry/pantry.html",
        {
            "form": form,
            "items": PantryItem.objects.filter(owner=request.user),
            "recent_consumptions": (
                MealConsumption.objects.filter(
                    planned_meal__owner=request.user,
                    status=MealConsumption.Status.COOKED,
                )
                .select_related("planned_meal__recipe")
                .prefetch_related("entries")[:6]
            ),
        },
    )


@login_required
def pantry_update(request, pk):
    item = get_object_or_404(PantryItem, pk=pk, owner=request.user)
    if request.method == "POST":
        form = PantryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    return redirect("pantry")
