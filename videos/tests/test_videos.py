import pytest
from ..models import Video
from django.urls import reverse
from django.contrib.auth.models import User
from auth_app.models import Userprofile
    
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
def test_get_video_list(client, token_obtain_pair_url, test_userprofile):
    login_data = {"email": test_userprofile.email, "password": "testpassword"}
    response = client.post(token_obtain_pair_url, login_data, content_type="application/json")
    url = reverse("videos")
    response = client.get(url)
    assert response.status_code == 200
