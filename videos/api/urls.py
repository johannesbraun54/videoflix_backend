from django.urls import path
from .views import VideosListView, VideoHLSPlaylistView, GetVideoHLSSegment, GetPortfolioVideoHLSSegment, PortfolioVideoHLSPlaylistView

urlpatterns = [
    path('video/', VideosListView.as_view(), name="video"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoHLSPlaylistView.as_view(), name="video-hls-playlist"),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', GetVideoHLSSegment.as_view(), name="video-hls-segment"),
    path('portfolio_video/<int:movie_id>/<str:resolution>/index.m3u8', PortfolioVideoHLSPlaylistView.as_view(), name="video-hls-playlist"),
    path('portfolio_video/<int:movie_id>/<str:resolution>/<str:segment>/', GetPortfolioVideoHLSSegment.as_view(), name="video-hls-segment")
]

 