from django.db import models

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(auto_created=True)
    title = models.CharField(max_length=256)
    file = models.FileField(upload_to=None, max_length=100)
    description = models.CharField(max_length=256)