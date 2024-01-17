from rest_framework import serializers
from .dep.auth import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed



class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length = 6)


    @staticmethod
    def validate_access_token( access_token ):
        google_user_data = Google.validate(access_token)
        try:
            user_id = google_user_data['sub']
        except:
            raise serializers.ValidationError("this token is invalid or has been expired")

        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail = "Could not verify the user")

        email = google_user_data['email']
        username = f"{google_user_data['given_name']}"
        # Conditionally append family name with an underscore if it's not empty
        family_name = google_user_data.get('family_name' , '')
        if family_name:
            username += f"_{family_name}"
        provider = "google"

        return register_social_user(provider, email, username, request)