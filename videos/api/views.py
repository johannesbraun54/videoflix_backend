from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import Video
from ..tasks import convert_video_into_hls
import django_rq
import os
from django.conf import settings


class VideosListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailView(APIView):
# 404 not found im frontend
    def get(self, request, movie_id, resolution):
        video = Video.objects.get(id=movie_id)

        m3u8_path = os.path.join(
            settings.MEDIA_ROOT, "videos", resolution, "index.m3u8"
        )

        if not os.path.exists(m3u8_path):
            raise Http404("Playlist not found")

        with open(m3u8_path, "r") as f:
            playlist_content = f.read()

        return HttpResponse(
            playlist_content, content_type="application/vnd.apple.mpegurl"
        )
