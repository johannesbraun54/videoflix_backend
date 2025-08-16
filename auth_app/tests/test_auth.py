from django.urls import reverse
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
def test_check_new_email_availability(client):
    url = reverse('email_availability')
    new_email = 'example@mail.de'
    response = client.post(url, {'email': new_email})
    assert response.status_code == 200
    assert response.data == {'exists': False}


@pytest.mark.django_db
def test_check_existing_email_availability(client):
    url = reverse('email_availability')
    exisisting_email = 'example@mail.de'
    User.objects.create_user(
        username='testuser', email=exisisting_email, password='testpassword')
    response = client.post(url, {'email': exisisting_email})
    assert response.status_code == 200
    assert response.data == {'exists': True}


def test_check_bad_request(client):
    url = reverse('email_availability')
    response = client.post(url)
    assert response.status_code == 400
    assert response.data == {"error": "Email is required"}

@pytest.mark.django_db
def test_registration(client):
    url = reverse('register')
    register_data = {
        "email": "user@example.com",
        "password": "securepassword",
        "confirmed_password": "securepassword"
    }
    response = client.post(url, register_data,  content_type="application/json")
    assert response.status_code == 201
    print("response.data",response.data)
    assert response.data['user']['email'] == 'user@example.com'

@pytest.mark.django_db
def test_bad_password(client):
    url = reverse('register')
    bad_register_data = {}
    response = client.post(url, bad_register_data, content_type="application/json")
    assert response.status_code == 400
    
@pytest.mark.django_db    
def test_login(client):
    url = reverse('token_obtain_pair')
    User.objects.create_user(username='testuser', email="user@example.com", password='testpassword')
    login_data = {"email":"user@example.com", "password":"testpassword"}
    response = client.post(url, login_data)
    assert response.status_code == 200