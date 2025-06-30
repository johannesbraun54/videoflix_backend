from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

def check_email_exists(email):
    """
    Check if the email exists in the database.
    """
    return User.objects.filter(email=email).exists()

class CheckEmailView(APIView):
       def post(self, request):
            email = request.data.get('email')
            if not email:
                return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

            if check_email_exists(email):
                return Response({"exists": True}, status=status.HTTP_200_OK)
            else:
                return Response({"exists": False}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    pass
