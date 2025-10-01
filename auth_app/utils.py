from .models import Userprofile
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def create_username(email):
    if email is not None:
        index = email.find("@")
        username = email[:index]
        return username
    return email

def create_userprofile(new_account):
    userprofile = Userprofile.objects.create(user=new_account, username=new_account.username, email=new_account.email)
    return userprofile

def encode_user_id_to_base64(user_id):
    data = str(user_id)  
    data_bytes = data.encode("utf-8") 
    uid_base64 = urlsafe_base64_encode(data_bytes)
    return uid_base64

def decode_uidb64_to_int(uidb64):
    uid_bytes = urlsafe_base64_decode(uidb64) 
    uid_str = uid_bytes.decode("utf-8")
    uid_int = int(uid_str)
    return uid_int

def token_is_valid(reset_token):
    if not reset_token:
        return False
    if reset_token.is_expired:
        reset_token.delete()
        return False
    return True
