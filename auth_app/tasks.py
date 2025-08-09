from authemail import wrapper
from authemail.models import send_multi_format_email

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

def send_mail(new_account_data):
    account = wrapper.Authemail()
    account.signup(email=new_account_data.email, password=new_account_data.password,
                           first_name="test", last_name="test")
    
def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': self.code
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    
    # new_email = SendVerifyMail()
    # new_email.send_email()
    

