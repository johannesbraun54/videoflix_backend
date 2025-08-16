from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from ..utils import encode_user_id_to_base64


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
    assert response.data['user']['email'] == 'user@example.com'
    
    existing_email_response = client.post(url, register_data,  content_type="application/json")
    assert existing_email_response.status_code == 400
    assert existing_email_response.data == {"username": ["A user with that username already exists."], 
                                            "email": ["Email is already in use"]}

    
    bad_password_register_data = {
        "email": "bad_user@example.com",
        "password": "securepassword",
        "confirmed_password": "wrong_password"
    }
    
    bad_password_response = client.post(url, bad_password_register_data,  content_type="application/json")
    assert bad_password_response.status_code == 400
    assert bad_password_response.data == {"confirmed_password": ["Passwords do not match"]}

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
    
    user_not_exists_login_data = {"email":"not_existing_user@example.com", "password":"testpassword"}
    bad_response = client.post(url, user_not_exists_login_data)
    assert bad_response.status_code == 400
    assert bad_response.data == { "non_field_errors": ["password or username wrong"]}

    
    bad_password_register_data = {
        "email":"user@example.com",
        "password": "wrong_password",
    }
    
    bad_password_response = client.post(url, bad_password_register_data,  content_type="application/json")
    assert bad_password_response.status_code == 400
    assert bad_password_response.data == { "non_field_errors": ["password or username wrong"]}
    
@pytest.mark.django_db        
def test_account_activation(client):
    
    url = reverse('register')
    register_data = {
        "email": "user@example.com",
        "password": "securepassword",
        "confirmed_password": "securepassword"
    }
    
    response = client.post(url, register_data,  content_type="application/json")
    print(response.data)
    assert response.status_code == 201
    
    user_id = response.data['user']['id']
    token = response.data['token']    
    
    url = reverse('activate', kwargs={'uidb64': encode_user_id_to_base64(user_id),'token':token})
    response = client.get(url)
    assert response.status_code == 200
