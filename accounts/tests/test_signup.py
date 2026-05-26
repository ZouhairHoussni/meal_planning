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
    assert response["Location"] == reverse("household_onboarding")
    assert get_user_model().objects.filter(username="zouhair").exists()

    onboarding = client.get(reverse("household_onboarding"))
    assert onboarding.status_code == 200
    assert "Set up your household" in onboarding.content.decode()
