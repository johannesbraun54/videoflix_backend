from django.urls import path
from .views import RegistrationView, check_email_availability

urlpatterns = [
    path('email_availability/',check_email_availability, name='email_availability'),
    path('registartion/', RegistrationView.as_view(), name='registration'),
]

