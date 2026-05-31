from django.urls import path

from . import views

urlpatterns = [
    path("", views.planner, name="planner"),
    path("add/", views.planner_add, name="planner_add"),
    path("<int:pk>/outcome/", views.planner_outcome, name="planner_outcome"),
    path("<int:pk>/delete/", views.planner_delete, name="planner_delete"),
]
