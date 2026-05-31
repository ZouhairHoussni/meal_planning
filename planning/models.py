from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from recipes.models import Recipe, Unit


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


class MealConsumption(models.Model):
    class Status(models.TextChoices):
        COOKED = "cooked", "Cooked"
        SKIPPED = "skipped", "Skipped"
        POSTPONED = "postponed", "Postponed"

    planned_meal = models.OneToOneField(
        PlannedMeal,
        on_delete=models.CASCADE,
        related_name="consumption",
    )
    status = models.CharField(max_length=16, choices=Status.choices)
    decided_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-decided_at"]

    def __str__(self):
        return f"{self.planned_meal}: {self.get_status_display()}"


class PantryConsumptionEntry(models.Model):
    consumption = models.ForeignKey(
        MealConsumption,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    name = models.CharField(max_length=160)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    unit = models.CharField(max_length=8, choices=Unit.choices, default=Unit.UNIT)

    class Meta:
        ordering = ["name", "unit"]

    def __str__(self):
        return f"{self.quantity:g} {self.unit} {self.name}"
