from authemail import wrapper

def send_mail(new_account_data):
    account = wrapper.Authemail()
    account.signup(email=new_account_data.email, password=new_account_data.password,
                           first_name="test", last_name="test")
    print("user registriert, email versendet")