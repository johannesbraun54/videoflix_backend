from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('registartion/', RegistrationView.as_view(), name='registration'),
]

