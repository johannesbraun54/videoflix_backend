from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import VideoflixUser
from .tasks import send_mail
import django_rq



# @receiver(post_save, sender=VideoflixUser)
# def user_post_save(sender, instance, created, **kwargs):
#     print("email wurde gesendet")
#     if created: 
#         queue = django_rq.get_queue("default", autocommit=True)
#         queue.enqueue(send_mail, instance)