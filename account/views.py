from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import User, OneTimePassword
from .serializers import UserRegisterSerializer , LoginUserSerializer , VerifyUserEmailSerializer , \
    PasswordResetSerializer , SetNewPasswordSerializer , LogoutUserSerializer , UserSerializer
from rest_framework.response import Response

from .utils.OTP import send_code_to_user
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class GetUsersPagination(PageNumberPagination):
    page_size = 8

class GetUsersApiView(ListAPIView):
    # queryset = User.objects.all().select_related("your-foreign-key")
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = GetUsersPagination



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
                }, status= status.HTTP_406_NOT_ACCEPTABLE)

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


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post( self, request ):
        serializer = self.serializer_class(data = request.data, context = {"request": request})
        serializer.is_valid(raise_exception = True)
        return Response({'message': 'a link has been send to your email'}, status = status.HTTP_200_OK)


# Todo combine them together when user clicked the link on email redirects to set-new password ant filled the uid and token in header
class PasswordResetConfirmView(GenericAPIView):

    def get( self, request, uidb64, token ):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'token is invalid or expired'}, status = status.HTTP_401_UNAUTHORIZED)

            return Response({'message': 'success', 'uidb64': uidb64, 'token': token}, status = status.HTTP_200_OK)

            # Needs rework on it
            # redirect_url = f'/set-new-password/?uidb64={uidb64}&token={token}'
            # return redirect(redirect_url)
        except DjangoUnicodeDecodeError:
            return Response({'message': 'token is invalid or expired'}, status = status.HTTP_401_UNAUTHORIZED)

class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch( self, request ):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            return Response({"message": "password reset was successful"}, status = status.HTTP_200_OK)


class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post( self, request ):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(serializer.error_messages, status = status.HTTP_400_BAD_REQUEST)