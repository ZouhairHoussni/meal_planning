import pytest
from decimal import Decimal
from django.urls import reverse

from households.models import Household


@pytest.mark.django_db
def test_onboarding_requires_login(client):
    response = client.get(reverse("household_onboarding"))

    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.django_db
def test_onboarding_creates_household_and_redirects_to_dashboard(client, django_user_model):
    user = django_user_model.objects.create_user(username="onboard-user", password="test-pass-123")
    client.force_login(user)

    response = client.post(
        reverse("household_onboarding"),
        {
            "name": "Zouhair home",
            "default_servings": "2",
            "adults_count": "1",
            "children_count": "0",
            "default_weekly_budget": "80.00",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("dashboard")
    household = Household.objects.get(owner=user)
    assert household.name == "Zouhair home"
    assert household.currency == "EUR"


@pytest.mark.django_db
def test_onboarding_rejects_invalid_budget(client, django_user_model):
    user = django_user_model.objects.create_user(username="invalid-budget-user", password="test-pass-123")
    client.force_login(user)

    response = client.post(
        reverse("household_onboarding"),
        {
            "name": "Zouhair home",
            "default_servings": "2",
            "adults_count": "1",
            "children_count": "0",
            "default_weekly_budget": "0.00",
        },
    )

    assert response.status_code == 200
    assert not Household.objects.filter(owner=user).exists()
    assert "Enter a weekly budget greater than zero" in response.content.decode()


@pytest.mark.django_db
def test_household_settings_updates_budget(client, django_user_model):
    user = django_user_model.objects.create_user(username="settings-user", password="test-pass-123")
    Household.objects.create(owner=user, name="Home", default_weekly_budget="80.00")
    client.force_login(user)

    response = client.post(
        reverse("household_settings"),
        {
            "name": "Home updated",
            "default_servings": "3",
            "adults_count": "2",
            "children_count": "1",
            "default_weekly_budget": "95.50",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("dashboard")
    household = Household.objects.get(owner=user)
    assert household.name == "Home updated"
    assert household.default_servings == 3
    assert household.default_weekly_budget == Decimal("95.50")
