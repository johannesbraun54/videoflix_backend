from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTCookieAuthentication(JWTAuthentication):
    
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        return self.get_user(self.get_validated_token(token)), self.get_validated_token(token)
