from django.urls import path
from .views import GoogleAuthView, GithubSignInView


urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="google"),
    path("github/", GithubSignInView.as_view(), name="google"),
]