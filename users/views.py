"""
User Authentication and Profile Views
Clean, production-ready implementation with JWT tokens
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer
)

User = get_user_model()


class RegisterAPIView(APIView):
    """
    User Registration Endpoint
    POST /api/v1/users/auth/register/
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        """Register a new user and return JWT tokens"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name
                    },
                    "tokens": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    User Login Endpoint
    POST /api/v1/users/auth/login/
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """Authenticate user and return JWT tokens"""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name
                    },
                    "tokens": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "message": "Login failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    User Logout Endpoint
    POST /api/v1/users/auth/logout/
    Requires: Authorization header with access token
    Body: {"refresh": "refresh_token_here"}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Blacklist the refresh token to logout user"""
        try:
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                return Response({
                    "success": False,
                    "message": "Refresh token is required",
                    "errors": {"refresh": ["This field is required"]}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                "success": True,
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                "success": False,
                "message": "Invalid or expired token",
                "errors": {"token": [str(e)]}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "Logout failed",
                "errors": {"detail": [str(e)]}
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    """
    User Profile Endpoint
    GET /api/v1/users/profile/ - Retrieve profile
    PUT /api/v1/users/profile/ - Full update
    PATCH /api/v1/users/profile/ - Partial update
    Requires: Authorization header with access token
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's profile"""
        serializer = ProfileSerializer(request.user)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user profile (full update)"""
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=False
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Return updated profile
            profile_data = ProfileSerializer(request.user).data
            
            return Response({
                "success": True,
                "message": "Profile updated successfully",
                "data": profile_data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "message": "Profile update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update user profile (partial update)"""
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Return updated profile
            profile_data = ProfileSerializer(request.user).data
            
            return Response({
                "success": True,
                "message": "Profile updated successfully",
                "data": profile_data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "message": "Profile update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshAPIView(APIView):
    """
    Token Refresh Endpoint
    POST /api/v1/users/auth/token/refresh/
    Body: {"refresh": "refresh_token_here"}
    Returns: New access and refresh tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Refresh access token using refresh token"""
        try:
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                return Response({
                    "success": False,
                    "message": "Refresh token is required",
                    "errors": {"refresh": ["This field is required"]}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new token from refresh token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)
            
            return Response({
                "success": True,
                "message": "Token refreshed successfully",
                "data": {
                    "access": access_token,
                    "refresh": new_refresh_token
                }
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                "success": False,
                "message": "Invalid or expired refresh token",
                "errors": {"token": [str(e)]}
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "Token refresh failed",
                "errors": {"detail": [str(e)]}
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """
    Change Password Endpoint
    POST /api/v1/users/profile/change-password/
    Requires: Authorization header with access token
    Body: {
        "old_password": "current_password",
        "new_password": "new_password",
        "new_password2": "confirm_new_password"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password2 = request.data.get("new_password2")
        
        # Validate required fields
        if not all([old_password, new_password, new_password2]):
            return Response({
                "success": False,
                "message": "All fields are required",
                "errors": {
                    "detail": ["old_password, new_password, and new_password2 are required"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check old password
        if not user.check_password(old_password):
            return Response({
                "success": False,
                "message": "Password change failed",
                "errors": {
                    "old_password": ["Current password is incorrect"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check password match
        if new_password != new_password2:
            return Response({
                "success": False,
                "message": "Password change failed",
                "errors": {
                    "new_password2": ["New passwords do not match"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password strength
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": "Password change failed",
                "errors": {
                    "new_password": list(e.messages)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({
            "success": True,
            "message": "Password changed successfully"
        }, status=status.HTTP_200_OK)