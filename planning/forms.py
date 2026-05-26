from django import forms

from recipes.models import Recipe

from .models import PlannedMeal


class PlannedMealForm(forms.ModelForm):
    class Meta:
        model = PlannedMeal
        fields = ["recipe", "date", "meal_type", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipe"].queryset = Recipe.objects.filter(owner=owner)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "class",
                "min-h-11 w-full rounded-xl border border-border bg-white px-3 py-2 text-sm text-text",
            )
