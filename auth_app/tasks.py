from authemail import wrapper
from authemail.models import SignupCode

def send_mail(new_account_data):
    account = wrapper.Authemail()
    account.signup(email=new_account_data.email, password=new_account_data.password,
                           first_name="test", last_name="test")
    
    new_user = SignupCode.objects.get(user=new_account_data.email)
    print("SignupCodeUser", new_user)
    return new_user.code
