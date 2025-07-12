def create_username(email):
    if email is not None:
        index = email.find("@")
        username = email[:index]
        return username
    return email