from django import forms

from .models import ShoppingItem


class ManualShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ["name", "quantity", "unit", "price", "brand", "store"]


class ShoppingItemToggleForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ["purchased"]


class ShoppingItemUpdateForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ["name", "quantity", "unit", "price", "brand", "store"]
