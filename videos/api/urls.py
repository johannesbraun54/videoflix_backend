from django.urls import path
from .views import VideosListView

urlpatterns = [
    # path('video_upload/', VideoUploadView.as_view(), name="video_upload" ),
    path('video/', VideosListView.as_view(), name="videos")
]
