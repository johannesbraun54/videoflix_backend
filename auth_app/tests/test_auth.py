from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Userprofile
import pytest
from ..utils import encode_user_id_to_base64
from ..models import PasswordResetToken


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
    assert "id" in response.data['user'] 
    assert "token" in response.data 
    
    
    
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
        username='user',
        email="user@example.com",
        password='testpassword'
    )
    
@pytest.fixture
def test_userprofile(test_user):
    return Userprofile.objects.create(
        user=test_user,
        username=test_user.username,
        email=test_user.email,
        is_verified=True
    )


@pytest.mark.django_db    
def test_login_success(client, token_obtain_pair_url, test_userprofile):
    
    login_data = {"email": "user@example.com", "password": "testpassword"}
    response = client.post(token_obtain_pair_url, login_data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == {
        "detail": "Login successful",
        "user": {
        "id": test_userprofile.user.id,
        "username": test_userprofile.username
    }
}
    
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
    assert response.data == {"message": "Account successfully activated."}

@pytest.mark.django_db        
def test_account_activation_with_wrong_credentials(client): 
    url = reverse('activate', kwargs={'uidb64': encode_user_id_to_base64(000),'token':"wrong_token123"})
    response = client.get(url)
    assert response.status_code == 400

@pytest.mark.django_db        
def test_success_token_refresh(client, token_obtain_pair_url, test_userprofile):
    
    login_data = {"email": "user@example.com", "password": "testpassword"}
    client.post(token_obtain_pair_url, login_data, content_type="application/json")
    
    refresh_url = reverse('token_refresh')
    response = client.post(refresh_url)
    
    assert response.status_code == 200
    assert response.data['detail'] == "Token refreshed"
    assert "access" in response.data
    
@pytest.mark.django_db        
def test_refresh_token_not_found(client):
    refresh_url = reverse('token_refresh')
    response = client.post(refresh_url)
    
    assert response.status_code == 400
    assert response.data == {"detail":"Refresh token not found"}

@pytest.mark.django_db      
def test_logout(client, token_obtain_pair_url, test_userprofile):    
    login_data = {"email": "user@example.com", "password": "testpassword"}
    client.post(token_obtain_pair_url, login_data, content_type="application/json")
    
    logout_url = reverse('logout')
    response = client.post(logout_url)
    assert response.status_code == 200
    assert response.data == {"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}
    
    
@pytest.mark.django_db      
def test_logout_failed(client):
    logout_url = reverse('logout')
    response = client.post(logout_url)
    assert response.status_code == 400
    assert response.data == {"detail": "No refresh token provided"}

@pytest.mark.django_db          
def test_reset_password(client, test_user):
    reset_url = reverse("password_reset")
    email_for_reset = {"email": test_user.email}
    response = client.post(reset_url, email_for_reset, content_type="application/json")
    assert response.status_code == 200 
    assert response.data == {"detail": "An email has been sent to reset your password."}

@pytest.mark.django_db              
def test_failed_reset_password(client):
    reset_url = reverse("password_reset")
    wrong_email_for_reset = {"email": "wrong_email@example.com"}
    response = client.post(reset_url, wrong_email_for_reset, content_type="application/json")
    assert response.status_code == 400 
    assert response.data == {"detail": "not existing user"}
    
@pytest.mark.django_db              
def test_confirm_password(client, test_user):
    reset_url = reverse("password_reset")
    email_for_reset = {"email": test_user.email}
    client.post(reset_url, email_for_reset, content_type="application/json")
    
    token = PasswordResetToken.objects.filter(user_id=test_user.id).first()
    confirm_url = reverse("password_confirm",kwargs={'uidb64': encode_user_id_to_base64(test_user.id),'token':token.key})
    data = {
                "new_password": "newsecurepassword",
                "confirm_password": "newsecurepassword"
            }
    
    response = client.post(confirm_url, data)
    assert response.status_code == 200 
    assert response.data == {"detail": "Your Password has been successfully reset."}
