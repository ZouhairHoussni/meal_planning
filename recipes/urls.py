from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("new/", views.recipe_create, name="recipe_new"),
    path("<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
]
