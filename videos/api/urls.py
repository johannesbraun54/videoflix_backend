from django.urls import path
from .views import VideosListView, VideoDetailView

urlpatterns = [
    path('video/', VideosListView.as_view(), name="video"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoDetailView.as_view(), name="video-detail")
]

 