from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeComponentFormSet, RecipeForm
from .models import Recipe


def save_recipe_formset(formset):
    components = formset.save(commit=False)
    for index, component in enumerate(components):
        component.position = index
        component.save()
    for deleted in formset.deleted_objects:
        deleted.delete()


@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(owner=request.user).prefetch_related("components")
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


@login_required
@transaction.atomic
def recipe_create(request):
    recipe = Recipe(owner=request.user)
    form = RecipeForm(request.POST or None, instance=recipe)
    formset = RecipeComponentFormSet(request.POST or None, instance=recipe, prefix="components")

    if request.method == "POST" and form.is_valid() and formset.is_valid():
        recipe = form.save(commit=False)
        recipe.owner = request.user
        recipe.save()
        formset.instance = recipe
        save_recipe_formset(formset)
        return redirect(recipe.get_absolute_url())

    return render(request, "recipes/recipe_form.html", {"form": form, "formset": formset, "is_edit": False})


@login_required
@transaction.atomic
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    form = RecipeForm(request.POST or None, instance=recipe)
    formset = RecipeComponentFormSet(request.POST or None, instance=recipe, prefix="components")

    if request.method == "POST" and form.is_valid() and formset.is_valid():
        recipe = form.save()
        save_recipe_formset(formset)
        return redirect(recipe.get_absolute_url())

    return render(request, "recipes/recipe_form.html", {"form": form, "formset": formset, "is_edit": True, "recipe": recipe})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related("components"),
        pk=pk,
        owner=request.user,
    )
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})
