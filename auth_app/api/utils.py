from ..models import Userprofile

def create_username(email):
    
    if email is not None:
        index = email.find("@")
        username = email[:index]
        return username
    return email

def create_userprofile(new_profile, token):
    userprofile = Userprofile.objects.create(user=new_profile, username=new_profile.username,email=new_profile.email, token=token)
    return userprofile