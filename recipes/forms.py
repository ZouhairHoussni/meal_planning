from django import forms
from django.forms import inlineformset_factory

from .models import Recipe, RecipeComponent


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description"]


class RecipeComponentForm(forms.ModelForm):
    class Meta:
        model = RecipeComponent
        fields = ["name", "quantity", "unit", "brand", "store", "note"]


RecipeComponentFormSet = inlineformset_factory(
    Recipe,
    RecipeComponent,
    form=RecipeComponentForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
