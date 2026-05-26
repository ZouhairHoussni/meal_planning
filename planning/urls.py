from django.urls import path

from . import views

urlpatterns = [
    path("", views.planner, name="planner"),
    path("add/", views.planner_add, name="planner_add"),
    path("<int:pk>/delete/", views.planner_delete, name="planner_delete"),
]
