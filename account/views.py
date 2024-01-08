
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import User, OneTimePassword
from .serializers import UserRegisterSerializer, LoginUserSerializer
from rest_framework.response import Response

from .utils.OTP import send_code_to_user


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post( self, request ):
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            user: User = serializer.data
            # ! send email validation code
            send_code_to_user(user['email'])
            return Response({
                "data": user,
                "message": f"hi {user['username']} thanks for choosing us , please check your inbox for activating account"
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    def post( self, request ):
        otpcode = request.get("otp")
        try:
            user_code_obj = OneTimePassword.objects.get(code = otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': f'account with email {user.email} verified successfully'
                }, status = status.HTTP_200_OK)

            return Response({
                'message': f'user {user.username} already verified'
            }, status= status.HTTP_204_NO_CONTENT)

        except OneTimePassword.DoesNotExist:
            return Response({'message': 'passcode not provided'}, status = status.HTTP_404_NOT_FOUND)
