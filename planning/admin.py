from django.contrib import admin

from .models import PlannedMeal


@admin.register(PlannedMeal)
class PlannedMealAdmin(admin.ModelAdmin):
    list_display = ("date", "meal_type", "recipe", "owner", "created_at")
    list_filter = ("date", "meal_type")
    search_fields = ("recipe__name", "owner__username", "note")
