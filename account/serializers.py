from rest_framework import serializers

from account.models import User , OneTimePassword
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed , NotFound
from django.urls import reverse
from .utils.email import send_email


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    password_confirm = serializers.CharField(max_length = 68, min_length = 6, write_only = True)

    class Meta:
        model= User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate( self, attrs ):
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if password != password_confirm:
            raise serializers.ValidationError("Password does not match!")

        return attrs

    def create(self, validated_data):
        # Pop the confirm_password
        validated_data.pop('password_confirm', None)

        user = User.objects.create_user(**validated_data)

        return user


class VerifyUserEmailSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(max_length = 24, write_only = True)

    class Meta:
        model = OneTimePassword
        fields = ["otp_code"]



class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 168, write_only = True)
    # Fields return
    email = serializers.EmailField(max_length = 255 , read_only = True)
    access_token = serializers.CharField(max_length = 255, read_only = True)
    refresh_token = serializers.CharField(max_length = 255, read_only = True)


    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'access_token', 'refresh_token']


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials.")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")

        user_tokens = user.generate_token()

        return {
            'email': user.email,
            'username': user.username,
            'access_token': str(user_tokens.get("access")),
            'refresh_token': str(user_tokens.get("refresh"))
        }

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        model = User
        fields = ['email']


    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            UIDbase64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get("request")
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs = {'uidb64': UIDbase64, 'token': token})
            abslink = f"http://{site_domain}{relative_link}"
            email_body = f"You requested password rest here is you link \n {abslink}"
            data = {
                'email_body': email_body,
                'email_subject': "Rest your password",
                'to_email': user.email
            }
            send_email(data = data)

            return super().validate(attrs)

        # Todo can be removed
        raise NotFound("no user found by this email")



class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 100, min_length = 6, write_only = True)
    confirm_password = serializers.CharField(max_length = 100, min_length = 6, write_only = True)
    uidb64 = serializers.CharField(write_only = True)
    token = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ["password", "confirm_password", "uidb64", "token"]


    def validate(self, attrs):
        try:
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has been expired buddy", 401)

            if password != confirm_password:
                raise AuthenticationFailed("confirm and password are not same")

            if user.check_password(password):
                raise AuthenticationFailed("New password cannot be the same as the current password.")


            user.set_password(password)
            user.save()
            return user
        except AuthenticationFailed as e:
            raise e  # Re-raise AuthenticationFailed exceptions
        except Exception as e:
            print(e)
            return AuthenticationFailed("link is invalid or has expired")
