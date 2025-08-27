from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'confirm_email',
            'first_name', 'last_name',
            'phone', 'address', 'city', 'country',
            'password', 'confirm_password'
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        confirm_email = attrs.get("confirm_email")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if email != confirm_email:
            raise serializers.ValidationError("Emails do not match")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_email")
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            phone=validated_data.get("phone"),
            address=validated_data.get("address"),
            city=validated_data.get("city"),
            country=validated_data.get("country"),
            password=validated_data.get("password"),
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68,write_only=True)
    full_name = serializers.CharField(max_length=255,read_only=True)
    access_token = serializers.CharField(max_length=255,read_only=True)
    refresh_token = serializers.CharField(max_length=255,read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']
        
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('invalid credentials try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        user_tokens = user.tokens()
        
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }

class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be numeric")
        return value
