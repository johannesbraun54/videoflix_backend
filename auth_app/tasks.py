from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import encode_user_id_to_base64
from django.conf import settings

def send_email(token, template, subject):
    template_name = template 
    verify_subject = subject
    
    context = {
        "frontend_url": settings.FRONTEND_URL,
        "token": token.key, 
        "uid": encode_user_id_to_base64(token.user.id),
        "username": token.user.username
    }
    
    html_message = render_to_string(template_name, context=context)
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(
        subject = verify_subject, 
        body = plain_message,
        from_email = None ,
        to= [token.user.email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    
    