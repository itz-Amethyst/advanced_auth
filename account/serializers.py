from rest_framework import serializers

from account.models import User


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