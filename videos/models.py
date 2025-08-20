from django.db import models

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(auto_created=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    file = models.FileField(upload_to='uploads/')
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=256)
    
    def __str__(self):
        return self.title