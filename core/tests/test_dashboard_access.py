import pytest
from django.urls import reverse


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
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "MealBudget" in content
    assert "Dashboard" in content
    assert "Phase 0 foundation" in content
    assert "Plan this week" in content
