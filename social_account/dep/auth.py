import string
import random

from google.auth.transport import requests
from google.oauth2 import id_token
from account.models import User
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from social_account.utils.response import send_response, authenticate_without_password_and_send_response


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request() )
            if "accounts.google.com" in id_info['iss']:
                return id_info
        except Exception as e:
            print(e)
            return "token is invalid or has expired"


def register_social_user(provider, email, username, request):
    user = User.objects.filter(email = email)
    # Log in the user
    if user.exists():
        if provider == user[0].auth_provider:
            return send_response(username, request)

        #? Note: here i manually added logic to logic the user if the email was same and user registered by manual way before
        elif user[0].auth_provider == "email":
            return authenticate_without_password_and_send_response(request = request, email = email)

        #! To check if it wasn't google and email way either warn user to login by that way
        else:
            raise AuthenticationFailed(detail = f"Please continue your login with {user[0].auth_provider} way")

    # Create user
    # ? check if that username didn't exist
    if User.objects.filter(username = username).exists():
        random_numbers = ''.join(random.choices(string.digits, k=4))
        username += random_numbers

    registered_user = User.objects.create_user(
        email = email ,
        username = username ,
        password = settings.SOCIAL_AUTH_PASSWORD
    )
    registered_user.auth_provider = provider
    registered_user.is_verified = True
    registered_user.save()
    return send_response(registered_user.username, request)