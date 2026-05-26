from django.urls import reverse


def test_core_route_names_resolve():
    assert reverse("dashboard") == "/dashboard/"
    assert reverse("household_onboarding") == "/household/onboarding/"
    assert reverse("household_settings") == "/household/settings/"
    assert reverse("login") == "/accounts/login/"
    assert reverse("logout") == "/accounts/logout/"
