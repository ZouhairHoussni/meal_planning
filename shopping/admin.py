from django.contrib import admin

from .models import ShoppingItem


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "unit", "price", "brand", "store", "source", "purchased", "owner", "updated_at")
    list_filter = ("source", "purchased", "unit", "store")
    search_fields = ("name", "brand", "store", "owner__username")
