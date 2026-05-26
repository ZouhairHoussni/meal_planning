from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from recipes.models import Unit


class ShoppingItem(models.Model):
    class Source(models.TextChoices):
        PLANNED = "planned", "Planned"
        MANUAL = "manual", "Manual"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_items")
    name = models.CharField(max_length=160)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    unit = models.CharField(max_length=8, choices=Unit.choices, default=Unit.UNIT)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    brand = models.CharField(max_length=120, blank=True, null=True, default="")
    store = models.CharField(max_length=120, blank=True, null=True, default="")
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.MANUAL)
    purchased = models.BooleanField(default=False)
    pantry_synced_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    pantry_synced_name = models.CharField(max_length=160, blank=True, default="")
    pantry_synced_unit = models.CharField(max_length=8, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["purchased", "name"]

    def __str__(self):
        return f"{self.name} ({self.quantity:g} {self.unit})"
