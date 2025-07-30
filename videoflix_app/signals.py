from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=Video)
def video_post_safe(sender, instance, created, **kwargs):
    print("video wurde gespeichert")
    if created:
        print("video created")
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, created, **kwargs):
    print("video deleted")