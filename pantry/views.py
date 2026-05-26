from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
        },
    )
