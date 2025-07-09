from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_repeated_password(self, value):
        password = self.initial_data.get('password')
        
        if password and value and password != value:
            raise serializers.ValidationError("Passwords do not match")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def save(self):
        
        pw = self.validated_data['password']
        
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        account.set_password(pw)
        account.save()
        return account
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        
        if not email or password: 
            raise serializers.ValidationError("email and password are required")
        if not user or user.password != password:
            raise serializers.ValidationError("password or username wrong")