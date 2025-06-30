from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('verif_email/', RegistrationView.as_view(), name='verif_email'),
    path('registartion/', RegistrationView.as_view(), name='registration'),
]

