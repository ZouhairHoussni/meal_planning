from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pantry/", include("pantry.urls")),
    path("planner/", include("planning.urls")),
    path("recipes/", include("recipes.urls")),
    path("shopping/", include("shopping.urls")),
    path("", include("core.urls")),
]
