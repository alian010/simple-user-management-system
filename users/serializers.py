"""
User Serializers for Authentication and Profile Management
Compatible with email-based User model
"""
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2']
        extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate(self, attrs):
        """Validate password match and strength"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Password fields do not match.'
            })

        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': list(e.messages)
            })

        return attrs

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with email
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Authenticate user credentials"""
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                'Both email and password are required.'
            )

        # Authenticate with email
        user = authenticate(
            request=self.context.get('request'),
            username=email.lower(),  # USERNAME_FIELD is email
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                'Invalid credentials. Please try again.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This account has been deactivated.'
            )

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (read-only)
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'created_at', 'updated_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    class Meta:
        model = User
        fields = ['full_name', 'email']
        extra_kwargs = {
            'email': {'required': False},
            'full_name': {'required': False}
        }

    def validate_email(self, value):
        """Validate email uniqueness (exclude current user)"""
        user = self.instance
        if User.objects.filter(email__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def update(self, instance, validated_data):
        """Update user profile"""
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance