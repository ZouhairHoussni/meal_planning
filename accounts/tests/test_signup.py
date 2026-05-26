import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_signup_creates_user_and_logs_them_in(client):
    response = client.post(
        reverse("signup"),
        {
            "username": "zouhair",
            "email": "zouhair@example.com",
            "password1": "a-secure-pass-123",
            "password2": "a-secure-pass-123",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("dashboard")
    assert get_user_model().objects.filter(username="zouhair").exists()

    dashboard = client.get(reverse("dashboard"))
    assert dashboard.status_code == 200
