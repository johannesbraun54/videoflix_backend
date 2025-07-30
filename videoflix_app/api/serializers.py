from rest_framework import serializers
from videoflix_app.models import Video

class VideoUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'