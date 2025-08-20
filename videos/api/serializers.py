from rest_framework import serializers
from videos.models import Video

class VideoUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'
        
class VideoListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'