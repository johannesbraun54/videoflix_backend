from .models import Userprofile
from django.utils.http import urlsafe_base64_encode

def create_username(email):
    
    if email is not None:
        index = email.find("@")
        username = email[:index]
        return username
    return email

def create_userprofile(new_profile, token):
    userprofile = Userprofile.objects.create(user=new_profile, username=new_profile.username,email=new_profile.email, token=token)
    return userprofile

def encode_user_id_to_base64(user_id):
    data = str(user_id)  
    data_bytes = data.encode("utf-8") 
    uid_base64 = urlsafe_base64_encode(data_bytes)
    return uid_base64