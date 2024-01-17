from django.conf import settings
from django.contrib.auth import authenticate , login
from rest_framework.exceptions import AuthenticationFailed

from account.models import User


def send_response(email):
    login_user = authenticate(email = email , password = settings.SOCIAL_AUTH_PASSWORD)
    user_tokens = login_user.generate_token()
    return {
        'email': login_user.email ,
        'username': login_user.username ,
        'access_token': str(user_tokens.get("access")) ,
        'refresh_token': str(user_tokens.get("refresh"))
    }

# Todo make this more secure
def authenticate_without_password(request, email):
    user = User.objects.filter(email = email).first()

    if user is not None:
        # Log in the user and generate datas in cookies
        login(request , user)
        user_tokens = user.generate_token()
        return {
            'email': user.email,
            'username': user.username,
            'access_token':  str(user_tokens.get("access")),
            'refresh_token': str(user_tokens.get("refresh"))
        }
    else:
        raise AuthenticationFailed(detail = "Authentication failed. User credentials are incorrect.")