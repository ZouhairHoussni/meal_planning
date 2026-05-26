import pytest
from django.urls import reverse

from households.models import Household
from shopping.models import ShoppingItem


@pytest.mark.django_db
def test_dashboard_redirects_anonymous_user(client):
    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.django_db
def test_dashboard_renders_authenticated_shell(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="planner",
        email="planner@example.com",
        password="test-pass-123",
    )
    Household.objects.create(owner=user, name="Planner home", default_weekly_budget="80.00")
    ShoppingItem.objects.create(owner=user, name="Pasta", quantity="1", unit="unit", price="12.50")
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "MealBudget" in content
    assert "Dashboard" in content
    assert "Weekly budget" in content
    assert "EUR 80.00" in content
    assert "EUR 67.50 left" in content
    assert "Plan this week" in content


@pytest.mark.django_db
def test_dashboard_redirects_authenticated_user_without_household(client, django_user_model):
    user = django_user_model.objects.create_user(username="new-user", password="test-pass-123")
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response["Location"] == reverse("household_onboarding")
