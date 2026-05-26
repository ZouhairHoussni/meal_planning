from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Household(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_households")
    name = models.CharField(max_length=120)
    default_servings = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1)])
    adults_count = models.PositiveSmallIntegerField(default=0)
    children_count = models.PositiveSmallIntegerField(default=0)
    default_weekly_budget = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(max_length=3, default="EUR")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["owner"], name="unique_mvp_household_per_owner"),
            models.CheckConstraint(condition=Q(default_servings__gte=1), name="household_default_servings_positive"),
            models.CheckConstraint(condition=Q(default_weekly_budget__gt=0), name="household_weekly_budget_positive"),
            models.CheckConstraint(condition=Q(currency="EUR"), name="household_currency_eur"),
        ]

    def __str__(self):
        return self.name
