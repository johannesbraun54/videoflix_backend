from django.dispatch import receiver
from django.db.models.signals import post_save

from videoflix_app.tasks import convert_480p
from .models import VideoflixUser

@receiver(post_save, sender=VideoflixUser)

def video_post_save(sender, instance, created, **kwargs):
    print("email wurde gesendet")
    if created: 
        print("email wurde gesendet")
        convert_480p(instance.video_file.path)