from django.db import models
from django.contrib.auth.models import User


# class VideoflixUser(EmailAbstractUser):
#     # Custom fields
# 	username = models.CharField(max_length=150, unique=True)
# 	# Required
# 	objects = EmailUserManager()

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    token = models.CharField(max_length=150, unique=True)


