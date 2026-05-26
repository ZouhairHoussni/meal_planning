from decimal import Decimal

from django import forms

from .models import Household


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ["name", "default_servings", "adults_count", "children_count", "default_weekly_budget"]
        labels = {
            "name": "Household name",
            "default_servings": "Default servings",
            "adults_count": "Adults",
            "children_count": "Children",
            "default_weekly_budget": "Weekly budget",
        }

    def clean_default_weekly_budget(self):
        value = self.cleaned_data["default_weekly_budget"]
        if value <= Decimal("0.00"):
            raise forms.ValidationError("Enter a weekly budget greater than zero")
        return value

    def clean_default_servings(self):
        value = self.cleaned_data["default_servings"]
        if value < 1:
            raise forms.ValidationError("Enter at least one serving")
        return value
