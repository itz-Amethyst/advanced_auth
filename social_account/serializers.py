from rest_framework import serializers
from .dep.auth import Google, register_social_user
from .dep.github import Github
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError



class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length = 6)


    def validate_access_token( self, access_token ):
        google_user_data = Google.validate(access_token)
        request = self.context.get('request')
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
    

class GithubOauthSerializer(serializers.Serializer):
    code = serializers.CharField(min_length = 2)


    def validate_code(self, code):
        access_token = Github.exchange_code_for_token(code)
        request = self.context.get('request')


        if access_token:
            # Todo
            user = Github.retrieve_github_user(access_token)
            full_name = user['name']
            email = user['email']
            # Divide 
            names = full_name.split(" ")
            first_name = names[1]
            last_name = names[0]
            provider = "github"
            return register_social_user(provider, email , username, request)

        else:
            raise ValidationError("token is invalid or has been expired")
