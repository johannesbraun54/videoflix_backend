from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTCookieAuthentication(JWTAuthentication):
    """
    Custom authentication class to read JWT from cookies instead from Authorization-Header.
    """
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        return self.get_user(self.get_validated_token(token)), self.get_validated_token(token)
