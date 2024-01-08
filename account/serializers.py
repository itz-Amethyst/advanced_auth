from rest_framework import serializers

from account.models import User , OneTimePassword
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


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