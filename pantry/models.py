from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from recipes.models import Unit


class PantryItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pantry_items")
    name = models.CharField(max_length=160)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    unit = models.CharField(max_length=8, choices=Unit.choices, default=Unit.UNIT)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "name", "unit"], name="unique_pantry_item_per_owner_unit"),
        ]

    def __str__(self):
        return f"{self.name} ({self.quantity:g} {self.unit})"
