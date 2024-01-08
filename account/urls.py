from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, CheckIfLoggedIn

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("verify/", VerifyUserEmail.as_view(), name='verify'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("profile/", CheckIfLoggedIn.as_view(), name='profile'),
]