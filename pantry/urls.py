from django.urls import path

from . import views

urlpatterns = [
    path("", views.pantry, name="pantry"),
    path("<int:pk>/update/", views.pantry_update, name="pantry_update"),
]
