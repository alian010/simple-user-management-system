"""
User App URL Configuration
"""
from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    TokenRefreshAPIView,
    ChangePasswordAPIView
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    
    # Profile endpoints
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]