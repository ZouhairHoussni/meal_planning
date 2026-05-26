from django.urls import path

from . import views

urlpatterns = [
    path("", views.shopping_list, name="shopping"),
    path("add/", views.shopping_add_manual, name="shopping_add_manual"),
    path("<int:pk>/update/", views.shopping_update, name="shopping_update"),
    path("<int:pk>/toggle/", views.shopping_toggle, name="shopping_toggle"),
]
