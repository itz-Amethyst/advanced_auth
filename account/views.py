
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .models import User, OneTimePassword
from .serializers import UserRegisterSerializer , LoginUserSerializer , VerifyUserEmailSerializer
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
    serializer_class = VerifyUserEmailSerializer

    def post( self, request ):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            try:
                user_code_obj = OneTimePassword.objects.get(code = serializer.validated_data['otp_code'])
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
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginUserView(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post( self, request ):
        serializer = self.serializer_class(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class CheckIfLoggedIn(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get( self, request ):
        return Response({'message': "user is logged in."}, status = status.HTTP_200_OK)
