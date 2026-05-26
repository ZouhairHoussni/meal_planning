from django.contrib import admin

from .models import Household


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "default_weekly_budget", "currency", "default_servings", "updated_at")
    list_filter = ("currency",)
    search_fields = ("name", "owner__username", "owner__email")
