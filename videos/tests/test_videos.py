import pytest
from ..models import Video
from django.urls import reverse



def test_video_get(client):
    url = reverse("videos")
    response = client.get(url)
    assert response.status_code == 200
