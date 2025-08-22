from django.urls import path
from .views import VideosListView, VideoHLSPlaylistView, GetVideoHLSSegment

urlpatterns = [
    path('video/', VideosListView.as_view(), name="video"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoHLSPlaylistView.as_view(), name="video-hls-playlist"),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', GetVideoHLSSegment.as_view(), name="video-hls-segment")
]

 