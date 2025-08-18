from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from ..utils import encode_user_id_to_base64


@pytest.fixture
def email_availability_url():
    url = reverse('email_availability')
    return url

@pytest.mark.django_db
def test_check_new_email_availability(client, email_availability_url):
    new_email = 'example@mail.de'
    response = client.post(email_availability_url, {'email': new_email})
    assert response.status_code == 200
    assert response.data == {'exists': False}


@pytest.mark.django_db
def test_check_existing_email_availability(client, email_availability_url):
    exisisting_email = 'example@mail.de'
    User.objects.create_user(
        username='testuser', email=exisisting_email, password='testpassword')
    response = client.post(email_availability_url, {'email': exisisting_email})
    assert response.status_code == 200
    assert response.data == {'exists': True}


def test_check_bad_request(client, email_availability_url):
    response = client.post(email_availability_url)
    assert response.status_code == 400
    assert response.data == {"error": "Email is required"}

@pytest.fixture
def register_url():
    url = reverse('register')
    return url

@pytest.fixture
def valid_register_data():
    return {
        "email": "user@example.com",
        "password": "securepassword",
        "confirmed_password": "securepassword"
    }

@pytest.mark.django_db
def test_registration_success(client, register_url, valid_register_data):
    response = client.post(register_url, valid_register_data, content_type="application/json")

    assert response.status_code == 201
    assert response.data['user']['email'] == "user@example.com"
    
    
    
@pytest.mark.django_db
def test_registration_duplicate_email(client, register_url, valid_register_data):

    User.objects.create_user(username="user", email="user@example.com", password="securepassword")
    
    response = client.post(register_url, valid_register_data, content_type="application/json")

    assert response.status_code == 400
    assert "email" in response.data
    
@pytest.mark.django_db
def test_registration_password_missmatch(client, register_url):
    bad_password_data = {
        "email": "bad_user@example.com",
        "password": "securepassword",
        "confirmed_password": "wrong_password"
    }
    response = client.post(register_url, bad_password_data, content_type="application/json")

    assert response.status_code == 400
    assert response.data == {"confirmed_password": ["Passwords do not match"]}
    
@pytest.fixture
def token_obtain_pair_url():
    return reverse('token_obtain_pair')

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email="user@example.com",
        password='testpassword'
    )


@pytest.mark.django_db    
def test_login_success(client, token_obtain_pair_url, test_user):
    login_data = {"email": "user@example.com", "password": "testpassword"}
    response = client.post(token_obtain_pair_url, login_data, content_type="application/json")
    assert response.status_code == 200


@pytest.mark.django_db    
def test_login_user_not_exists(client, token_obtain_pair_url):
    login_data = {"email": "not_existing_user@example.com", "password": "testpassword"}
    response = client.post(token_obtain_pair_url, login_data, content_type="application/json")
    assert response.status_code == 400
    assert response.data == {"non_field_errors": ["password or username wrong"]}


@pytest.mark.django_db    
def test_login_wrong_password(client, token_obtain_pair_url, test_user):
    bad_password_data = {"email": "user@example.com", "password": "wrong_password"}
    response = client.post(token_obtain_pair_url, bad_password_data, content_type="application/json")
    assert response.status_code == 400
    assert response.data == {"non_field_errors": ["password or username wrong"]}

    
@pytest.mark.django_db        
def test_account_activation(client, register_url, valid_register_data):
    
    response = client.post(register_url, valid_register_data,  content_type="application/json")
    user_id = response.data['user']['id']
    token = response.data['token']    
    
    url = reverse('activate', kwargs={'uidb64': encode_user_id_to_base64(user_id),'token':token})
    response = client.get(url)
    assert response.status_code == 200
