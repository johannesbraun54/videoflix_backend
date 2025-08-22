from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from .serializers import VideoSerializer
from rest_framework import generics
from ..models import Video
import os
from django.conf import settings


class VideosListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailView(APIView):
    def get(self, request, movie_id, resolution):

        m3u8_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(movie_id), resolution, "index.m3u8"
        )

        if not os.path.exists(m3u8_path):
            raise Http404("Playlist not found")

        with open(m3u8_path, "r") as f:
            playlist_content = f.read()

        return HttpResponse(
            playlist_content, content_type="application/vnd.apple.mpegurl"
        )
