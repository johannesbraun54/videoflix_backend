# from authemail import wrapper
# from authemail.models import send_multi_format_email

import base64
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Userprofile
from django.utils.http import urlsafe_base64_encode

def send_new_signup_email(new_account):
    template_name = "signup_email.html" 
    verify_subject = "Verify your Videoflix account"
    
    data = str(new_account.id)
    data_bytes = data.encode("utf-8")
    bytes = base64.b64encode(data_bytes)
    uid_base64 = urlsafe_base64_encode(bytes)
    
    context = {
        "token": new_account.token, 
        "uid": uid_base64
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


### encode uid to base64

# class SendVerifyMail(AbstractBaseCode):
    
#     def send_email(self, prefix):
#         ctxt = {
#             'email': self.user.email,
#             'first_name': self.user.first_name,
#             'last_name': self.user.last_name,
#             'token': self.code,
#             'uid': ''
#         }
        
#         send_multi_format_email(prefix, ctxt, target_email=self.user.email)

#         def __str__(self):
#             return self.code
        
#         return super().send_email(prefix)

# def send_mail(new_account_data):
#     account = wrapper.Authemail()
#     account.signup(email=new_account_data.email, password=new_account_data.password,
#                            first_name="test", last_name="test")
    
# def send_email(self, prefix):
#         ctxt = {
#             'email': self.user.email,
#             'first_name': self.user.first_name,
#             'last_name': self.user.last_name,
#             'code': self.code
#         }
#         send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    
    # new_email = SendVerifyMail()
    # new_email.send_email()
    

