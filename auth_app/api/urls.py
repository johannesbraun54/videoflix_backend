from django.urls import path
from .views import RegistrationView, check_email_availability

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email_availability/',check_email_availability, name='email_availability'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]

