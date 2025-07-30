from django.urls import path
from .views import VideoUploadView

urlpatterns = [
    path('video_upload/', VideoUploadView.as_view(), name="video_upload" )
]
