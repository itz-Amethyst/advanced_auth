from django.urls import path
from .views import GoogleAuthView, GoogleAuthSerializer


urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="google"),
    path("github/", GoogleAuthSerializer.as_view(), name="google"),
]