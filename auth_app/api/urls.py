from django.urls import path
from .views import RegistrationView, check_email_availability, CookieTokenObtainPairView, CookieRefreshView, AccountActivationView, LogoutView


urlpatterns = [
    path('email_availability/',check_email_availability, name='email_availability'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', AccountActivationView.as_view(), name='activate'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'), 
]
