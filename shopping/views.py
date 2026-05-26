from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from pantry.services import sync_shopping_item_to_pantry

from .forms import ManualShoppingItemForm, ShoppingItemUpdateForm
from .models import ShoppingItem
from .selectors import shopping_summary_for_user
from .services import sync_planned_shopping_items


@login_required
def shopping_list(request):
    sync_planned_shopping_items(request.user)
    items = ShoppingItem.objects.filter(owner=request.user)
    return render(
        request,
        "shopping/shopping_list.html",
        {
            "items": items,
            "manual_form": ManualShoppingItemForm(),
            "unit_choices": ShoppingItem._meta.get_field("unit").choices,
            "summary": shopping_summary_for_user(request.user),
        },
    )


@login_required
def shopping_add_manual(request):
    if request.method == "POST":
        form = ManualShoppingItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.source = ShoppingItem.Source.MANUAL
            item.save()
    return redirect("shopping")


@login_required
def shopping_toggle(request, pk):
    item = get_object_or_404(ShoppingItem, pk=pk, owner=request.user)
    if request.method == "POST":
        item.purchased = not item.purchased
        item.save(update_fields=["purchased", "updated_at"])
        sync_shopping_item_to_pantry(item)
    return redirect("shopping")


@login_required
def shopping_update(request, pk):
    item = get_object_or_404(ShoppingItem, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ShoppingItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            if item.purchased or item.pantry_synced_quantity:
                sync_shopping_item_to_pantry(item)
    return redirect("shopping")
