from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utils import encode_user_id_to_base64

def send_new_signup_email(activation_token):
    template_name = "signup_email.html" 
    verify_subject = "Verify your Videoflix account"
    
    context = {
        "token": activation_token.key, 
        "uid": encode_user_id_to_base64(activation_token.user.id)
    }
    
    html_message = render_to_string(template_name, context=context)
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(
        subject = verify_subject, 
        body = plain_message,
        from_email = None ,
        to= [activation_token.user.email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    
    
def send_password_reset_email(reset_token):
    template_name = "reset_password.html" 
    verify_subject = "Reset your Password"
    
    context = {
        "token": reset_token.key,
         "uid": encode_user_id_to_base64(reset_token.user.id)
    }
    
    html_message = render_to_string(template_name, context=context)
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(
        subject = verify_subject, 
        body = plain_message,
        from_email = None,
        to= [reset_token.user.email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    
    