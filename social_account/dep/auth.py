from google.auth.transport import requests
from google.oauth2 import id_token
from account.models import User
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from social_account.utils.response import send_response


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request)
            if "accounts.google.com" in id_info['iss']:
                return id_info
        except Exception as e:
            print(e)
            return "token is invalid or has expired"


def register_social_user(provider, email, username):
    user = User.objects.filter(email = email)
    # Log in the user
    if user.exists():
        if provider == user[0].auth_provider:
           return send_response(email)

        else:
            raise AuthenticationFailed(detail = f"Please continue your login with {user[0].auth_provider}")

    # Create user
    registered_user = User.objects.create_user(
        email = email ,
        username = username ,
        password = settings.SOCIAL_AUTH_PASSWORD
    )
    registered_user.auth_provider = provider
    registered_user.is_verified = True
    registered_user.save()
    return send_response(email)