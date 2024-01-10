from django.conf import settings
from django.contrib.auth import authenticate


def send_response(email):
    login_user = authenticate(email = email , password = settings.SOCIAL_AUTH_PASSWORD)
    user_tokens = login_user.generate_token()
    return {
        'email': login_user.email ,
        'username': login_user.username ,
        'access_token': str(user_tokens.get("access")) ,
        'refresh_token': str(user_tokens.get("refresh"))
    }