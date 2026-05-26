from django.contrib import admin

from .models import PantryItem


@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "unit", "owner", "updated_at")
    search_fields = ("name", "owner__username")
