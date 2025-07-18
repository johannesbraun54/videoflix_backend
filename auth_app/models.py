from django.db import models
from django.contrib.auth.models import User
from authemail.models import EmailUserManager, EmailAbstractUser

class VideoflixUser(EmailAbstractUser):
    # Custom fields
	date_of_birth = models.DateField('Date of birth', null=True, blank=True)
	username = models.CharField(max_length=150, unique=True)
	# Required
	objects = EmailUserManager()