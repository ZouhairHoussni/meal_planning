from django.contrib import admin

from .models import MealConsumption, PantryConsumptionEntry, PlannedMeal


@admin.register(PlannedMeal)
class PlannedMealAdmin(admin.ModelAdmin):
    list_display = ("date", "meal_type", "recipe", "owner", "created_at")
    list_filter = ("date", "meal_type")
    search_fields = ("recipe__name", "owner__username", "note")


class PantryConsumptionEntryInline(admin.TabularInline):
    model = PantryConsumptionEntry
    extra = 0


@admin.register(MealConsumption)
class MealConsumptionAdmin(admin.ModelAdmin):
    list_display = ("planned_meal", "status", "decided_at")
    list_filter = ("status", "decided_at")
    search_fields = ("planned_meal__recipe__name", "planned_meal__owner__username")
    inlines = (PantryConsumptionEntryInline,)
