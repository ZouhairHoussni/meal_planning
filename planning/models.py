from django.conf import settings
from django.db import models

from recipes.models import Recipe


class PlannedMeal(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", "Breakfast"
        LUNCH = "lunch", "Lunch"
        DINNER = "dinner", "Dinner"
        EXTRA = "extra", "Extra"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="planned_meals")
    date = models.DateField()
    meal_type = models.CharField(max_length=16, choices=MealType.choices)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="planned_meals")
    note = models.CharField(max_length=160, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "date", "meal_type", "recipe"],
                name="unique_recipe_once_per_owner_slot",
            )
        ]

    def __str__(self):
        return f"{self.date} {self.meal_type}: {self.recipe}"
