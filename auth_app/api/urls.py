from django.urls import path
from .views import RegistrationView, check_email_availability, CookieTokenObtainPairView, CookieRefreshView
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('email_availability/',check_email_availability, name='email_availability'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
]

