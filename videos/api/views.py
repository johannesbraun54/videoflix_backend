from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from .serializers import VideoSerializer
from rest_framework import generics
from ..models import Video
import os
from django.conf import settings
from rest_framework.permissions import AllowAny



class VideosListView(generics.ListAPIView):
    """
    Views a List of all Public Videos.
    """
    queryset = Video.objects.filter(is_public=True)
    serializer_class = VideoSerializer


class VideoHLSPlaylistView(APIView):
    """
    Serves the HLS playlist for a given video,
    accordingly to the requested resolution.
    """
    def get(self, request, movie_id, resolution):

        index_m3u8_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(movie_id), resolution, "index.m3u8"
        )

        if not os.path.exists(index_m3u8_path):
            raise Http404("Playlist not found")

        with open(index_m3u8_path, "r") as f:
            playlist_content = f.read()

        return HttpResponse(
            playlist_content, content_type="application/vnd.apple.mpegurl"
        )
        
class GetVideoHLSSegment(APIView):
    """
    Returns a specific HLS segment for a given video and resolution.
    """
    def get(self, request, movie_id, resolution, segment):
        segment_path = os.path.join(settings.MEDIA_ROOT, "videos", str(movie_id), resolution, segment)
        
        if not os.path.exists(segment_path):
            raise Http404("Segment not found")
        
        with open(segment_path, "rb") as f:
            segment_file = f.read()
            
        return HttpResponse(
            segment_file, content_type="video/mp2t"
        )


class PortfolioVideoHLSPlaylistView(APIView):
    """
    I am using this view to serve HLS playlists for my personal portfolio videos.
    Portfolio videos has set Public=False. They are not listed in the VideosListView.
    """
    
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request, movie_id, resolution):

        index_m3u8_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(movie_id), resolution, "index.m3u8"
        )

        if not os.path.exists(index_m3u8_path):
            raise Http404("Playlist not found")

        with open(index_m3u8_path, "r") as f:
            playlist_content = f.read()

        return HttpResponse(
            playlist_content, content_type="application/vnd.apple.mpegurl"
        )
        
class GetPortfolioVideoHLSSegment(APIView):
    """
    Returns a specific HLS segment for a given portfolio video and resolution.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request, movie_id, resolution, segment):
        segment_path = os.path.join(settings.MEDIA_ROOT, "videos", str(movie_id), resolution, segment)
        
        if not os.path.exists(segment_path):
            raise Http404("Segment not found")
        
        with open(segment_path, "rb") as f:
            segment_file = f.read()
            
        return HttpResponse(
            segment_file, content_type="video/mp2t"
        )
