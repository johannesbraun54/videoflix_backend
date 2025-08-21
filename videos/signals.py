from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .tasks import convert_480p, generate_thumbnail
import os
import django_rq
from django.conf import settings


@receiver(post_save, sender=Video)
def video_post_safe(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(convert_480p, instance.file.path)
        queue.enqueue(generate_thumbnail, instance.id)
    
    
@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.file:
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{instance.id}.jpg")
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            print("(instance.file",instance.file)
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)

### delete all convert versions 