# backend/api/urls.py
from django.urls import path
from ...api.user_api import UserLoginAPIView

urlpatterns = [
    # Points to UserLoginAPI, to handle authentication
    path('users/login/api/', UserLoginAPIView.as_view(), name='user-login'),
]
