from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer

@api_view(['POST'])
def check_email_availability(request):
    
    if request.method == 'POST':
        print(request.data)
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
class HelloWorldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
    

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class CookieTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_execption=True)
        
        refresh = serializer.validated_data['refresh'] # token for refreshing
        access = serializer.validated_data['access'] # token for accessing protected resources
        response = Response({"message":"login successful"}, status=status.HTTP_200_OK)

        response.set_cookie( 
            key='access_token',
            value=access,
            httponly=True,
            secure=True,  
            samesite='Lax',
        )
        
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,  
            samesite='Lax',
        )
        
        response.data = {
            'message': 'Login successful',
        }

        return response
    
class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detail":"Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data={'refresh': refresh_token}) # warum so? weil der TokenRefreshView erwartet, dass die Daten in einem bestimmten Format sind, und wir hier den refresh token aus den Cookies holen müssen.
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail":"Refresh token invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data.get('access') # warum ist das so? weil der TokenRefreshView den access token aus dem refresh token generiert und wir ihn hier brauchen, um ihn in einem Cookie zu setzen.
        response = Response({"message":"access token refreshed"}, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  
            samesite='Lax',
        )
        
        return response