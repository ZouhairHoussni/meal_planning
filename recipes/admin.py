from django.contrib import admin

from .models import Recipe, RecipeComponent


class RecipeComponentInline(admin.TabularInline):
    model = RecipeComponent
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "component_count", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("name", "description", "components__name", "owner__username")
    inlines = [RecipeComponentInline]

    @admin.display(description="components")
    def component_count(self, obj):
        return obj.components.count()


@admin.register(RecipeComponent)
class RecipeComponentAdmin(admin.ModelAdmin):
    list_display = ("name", "recipe", "quantity", "unit", "brand", "store")
    list_filter = ("store", "brand", "unit")
    search_fields = ("name", "brand", "store", "recipe__name")
