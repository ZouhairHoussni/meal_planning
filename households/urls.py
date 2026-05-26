from django.urls import path

from . import views

urlpatterns = [
    path("onboarding/", views.onboarding, name="household_onboarding"),
    path("settings/", views.settings, name="household_settings"),
]
