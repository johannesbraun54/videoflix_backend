from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VideoUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import Video

class VideosListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Video.objects.all()
    serializer_class = VideoUploadSerializer



























# class VideoUploadView(APIView):
    
#     def post(self, request, format=None):
#         serializer = VideoUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)