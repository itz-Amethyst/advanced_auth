from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, CheckIfLoggedIn, PasswordResetConfirmView, PasswordResetView, SetNewPassword, LogoutUserView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("verify/", VerifyUserEmail.as_view(), name='verify'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("profile/", CheckIfLoggedIn.as_view(), name='profile'),
    path("password-reset/", PasswordResetView.as_view(), name='password-reset'),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("set-new-password/" , SetNewPassword.as_view() , name = 'set-new-password') ,
    path("logout/" , LogoutUserView.as_view() , name = 'logout') ,

]