from django.urls import path
from .views import RegistrationView, check_email_availability, CookieTokenObtainPairView, CookieRefreshView, AccountActivationView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('email_availability/',check_email_availability, name='email_availability'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', AccountActivationView.as_view(), name='activate'),
]
