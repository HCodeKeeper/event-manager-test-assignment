import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    email = "user1@gmail.com"
    password = "password"
    user = django_user_model.objects.create_user(email=email, password=password)
    return user


@pytest.mark.django_db
def test_register_user_without_name(api_client):
    email = "user1@gmail.com"
    password = "password"
    response = api_client.post(
        "/api/auth/register",
        {
            "email": email,
            "password": password,
        },
        format="json",
    )
    assert response.status_code == 201
    user = User.objects.get(email=email)
    assert user.check_password(password)
    assert user.first_name == ""
    assert user.last_name == ""


@pytest.mark.django_db
def test_register_user_with_name(api_client):
    email = "user1@gmail.com"
    password = "password"
    first_name = "John"
    last_name = "Doe"
    response = api_client.post(
        "/api/auth/register",
        {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
        format="json",
    )
    assert response.status_code == 201
    user = User.objects.get(email=email)
    assert response.data["user"]["id"] == user.id
    assert user.first_name == first_name
    assert user.last_name == last_name


@pytest.mark.django_db
def test_login(api_client, user, test_password):
    response = api_client.post(
        "/api/auth/login",
        {
            "email": user.email,
            "password": test_password,
        },
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["access"]
    assert response.data["refresh"]


@pytest.mark.django_db
def test_login_wrong_password(api_client, user):
    response = api_client.post(
        "/api/auth/login",
        {
            "email": user.email,
            "password": "wrongpassword",
        },
        format="json",
    )
    assert response.status_code == 401
