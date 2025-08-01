from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .tasks import convert_480p
import os

@receiver(post_save, sender=Video)
def video_post_safe(sender, instance, created, **kwargs):
    print("video wurde gespeichert")
    if created:
        convert_480p(instance.file.path)
        print("video created")
        
# @receiver(post_delete, sender=Video)
# def video_post_delete(sender, instance, created, **kwargs):
#     print("video deleted")
    
    
@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)