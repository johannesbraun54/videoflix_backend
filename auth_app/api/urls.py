from django.urls import path
from .views import RegistrationView, check_email_availability, CookieTokenObtainPairView, CookieRefreshView, AccountActivationView, LogoutView, PasswordResetView, ConfirmPasswordView


urlpatterns = [
    path('email_availability/',check_email_availability, name='email_availability'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', AccountActivationView.as_view(), name='activate'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/', DjangoPasswordResetView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/', ConfirmPasswordView.as_view(), name='password_confirm'),
]