from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser

class VideoflixUser(EmailAbstractUser):
    # Custom fields
	username = models.CharField(max_length=150, unique=True)
	# Required
	objects = EmailUserManager()