
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import User
from .serializers import UserRegisterSerializer
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
            # check
            send_code_to_user(user['email'])
            #! send email validation code
            return Response({
                "data": user,
                "message": f"hi {user['username']} thanks for choosing us , please check your inbox for activating account"
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
