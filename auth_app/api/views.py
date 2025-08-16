from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .utils import create_username, create_userprofile
from ..tasks import send_new_signup_email
import django_rq
import uuid
from ..models import Userprofile
from django.utils.http import urlsafe_base64_decode






@api_view(['POST'])
@permission_classes([AllowAny])
def check_email_availability(request):
    
    if request.method == 'POST':
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
        # request.data._mutable = True
        request.data['username'] = create_username(request.data.get('email', None))
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            
            new_account = serializer.save()
            new_account.is_active = False
            
            token = uuid.uuid4().hex
            
            queue = django_rq.get_queue("default", autocommit=True)
            queue.enqueue(send_new_signup_email, create_userprofile(new_account, token))
            
           
            data = { "user" :{
                'id': new_account.id,
                'email': new_account.email,
            } ,
               "token": token } 
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
class AccountActivationView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        
        uid_bytes = urlsafe_base64_decode(uidb64) 
        uid_str = uid_bytes.decode("utf-8")
        uid_int = int(uid_str)
        user = User.objects.filter(id=uid_int).first()
            
        if user:
            user.is_active = True
            user.save()
            return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)            
        else:
            return Response({"message": "Account activation failed."}, status=status.HTTP_400_BAD_REQUEST)          
    

class CookieTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)           
        refresh = serializer.validated_data['refresh'] # token for refreshing
        access = serializer.validated_data['access'] # token for accessing protected resources
        response =     Response({
                            "detail": "Login successful",
                            "user": {
                                "id": serializer.user.id,
                                "username": serializer.user.username
                            }
                            }, status=status.HTTP_200_OK)
        

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
        response = Response({
                            "detail": "Token refreshed",
                            "access": access_token
                            }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  
            samesite='Lax',
        )
        
        return response