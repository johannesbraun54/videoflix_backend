from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import VideoflixUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    
    confirmed_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = VideoflixUser
        fields = ('username', 'email', 'password', 'confirmed_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_confirmed_password(self, value):
        password = self.initial_data.get('password')
        
        if password and value and password != value:
            raise serializers.ValidationError("Passwords do not match")
        return value
    
    def validate_email(self, value):
        if VideoflixUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def save(self):
        
        pw = self.validated_data['password']
        
        account = VideoflixUser(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        account.set_password(pw)
        account.save()
        return account

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields.pop("username")
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = VideoflixUser.objects.get(email=email)
        
        try:
            user = VideoflixUser.objects.get(email=email)
        except VideoflixUser.DoesNotExist:
            raise serializers.ValidationError("password or username wrong")
        
        if not VideoflixUser.check_password(password):
            raise serializers.ValidationError("password or username wrong")
        
        data = super().validate({"username": user.username, "password": password})
        return data 
        