from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    token = models.CharField(max_length=150, unique=True) # sinnvoll ? 
    is_verified = models.BooleanField(default=False)


class PasswordResetToken(models.Model):
    key = models.CharField(max_length=255, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.timestamp + timedelta(hours=24)
