from rest_framework import serializers
from videos.models import Video
        
class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.
    """
    class Meta:
        model = Video
        fields = '__all__'