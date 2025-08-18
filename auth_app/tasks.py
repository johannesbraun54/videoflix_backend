from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import encode_user_id_to_base64

def send_new_signup_email(new_account):
    template_name = "signup_email.html" 
    verify_subject = "Verify your Videoflix account"
    
    context = {
        "token": new_account.token, 
        "uid": encode_user_id_to_base64(new_account.user.id)
    }
    
    html_message = render_to_string(template_name, context=context)
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(
        subject = verify_subject, 
        body = plain_message,
        from_email = None ,
        to= [new_account.email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    
    
def send_password_reset_email(user, token):
    template_name = "reset_password.html" 
    verify_subject = "Reset your Password"
    
    context = {
        "token": token,
         "uid": encode_user_id_to_base64(user.id)
    }
    
    html_message = render_to_string(template_name, context=context)
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(
        subject = verify_subject, 
        body = plain_message,
        from_email = None,
        to= [user.email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    
    