import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_primary_navigation_links_are_clickable(client, django_user_model):
    user = django_user_model.objects.create_user(username="nav", password="test-pass-123")
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    content = response.content.decode()
    assert f'href="{reverse("planner")}"' in content
    assert f'href="{reverse("shopping")}"' in content
    assert f'href="{reverse("recipe_list")}"' in content
    assert f'href="{reverse("pantry")}"' in content
