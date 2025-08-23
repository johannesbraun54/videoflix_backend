from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import (
    create_username,
    create_userprofile,
    decode_uidb64_to_int,
    token_is_valid,
)
from ..tasks import send_email
import django_rq
import uuid
from ..models import PasswordResetToken, AccountActivationToken


@api_view(["POST"])
@permission_classes([AllowAny])
def check_email_availability(request):

    if request.method == "POST":
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        request.data["username"] = create_username(request.data.get("email", None))
        serializer = RegistrationSerializer(data=request.data)
        # data = {}

        if serializer.is_valid():

            new_account = serializer.save()
            token = AccountActivationToken.objects.create(
                key=uuid.uuid4().hex, user=new_account
            )
            queue = django_rq.get_queue("default", autocommit=True)
            create_userprofile(new_account)
            queue.enqueue(
                send_email, token, "signup_email.html", "Verify your Videoflix account"
            )

            data = {
                "user": {
                    "id": new_account.id,
                    "email": new_account.email,
                },
                "token": token.key,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        activation_token = AccountActivationToken.objects.filter(key=token).first()
        user = User.objects.filter(id=decode_uidb64_to_int(uidb64)).first()

        if token_is_valid(activation_token):
            if user == activation_token.user:
                user.userprofile.is_verified = True
                user.userprofile.save()
                user.save()
                activation_token.delete()
                return Response(
                    {"message": "Account successfully activated."},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": "Account activation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CookieTokenObtainPairView(TokenObtainPairView):
    
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]
        response = Response(
            {
                "detail": "Login successful",
                "user": {
                    "id": serializer.user.id,
                    "username": serializer.user.username,
                },
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response


class CookieRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data={"refresh": refresh_token}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {"detail": "Refresh token invalid"}, status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = serializer.validated_data.get(
            "access"
        )  
        response = Response(
            {"detail": "Token refreshed", "access": access_token},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token == None:
            return Response({"detail": "No refresh token provided"}, status=400)

        refresh_token = RefreshToken(request.COOKIES.get("refresh_token"))
        refresh_token.blacklist()
        response = Response(
            {
                "detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."
            }
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class PasswordResetView(APIView):
    
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=400)
        user = User.objects.filter(email=email).first()

        if user and user.is_active:
            PasswordResetToken.objects.filter(user_id=user.id).delete()
            token = PasswordResetToken.objects.create(key=uuid.uuid4().hex, user=user)
            queue = django_rq.get_queue("default", autocommit=True)
            queue.enqueue(
                send_email, token, "reset_password.html", "Reset your Password"
            )

            return Response(
                {"detail": "An email has been sent to reset your password."}, status=200
            )
        return Response({"detail": "not existing user"}, status=400)


class ConfirmPasswordView(APIView):
    
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        reset_token = PasswordResetToken.objects.filter(key=token).first()
        user = User.objects.filter(id=decode_uidb64_to_int(uidb64)).first()

        if token_is_valid(reset_token) and user:
            if user == reset_token.user:
                new_password = request.data["new_password"]
                user.set_password(new_password)
                user.save()
                reset_token.delete()
                return Response(
                    {"detail": "Your Password has been successfully reset."}, status=200
                )
        return Response({"detail": "error occured"}, status=400)
