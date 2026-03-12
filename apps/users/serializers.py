from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer,
    TokenRefreshSlidingSerializer,
)

from .models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "is_email_verified",
            "is_phone_verified",
        )
        read_only_fields = ("id", "is_email_verified", "is_phone_verified")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "phone_number", "avatar")
        read_only_fields = ("id", "user")


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone_number")
        if not email and not phone:
            raise serializers.ValidationError("Either email or phone_number is required.")
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["phone_number"] = user.phone_number
        token["is_email_verified"] = user.is_email_verified
        token["is_phone_verified"] = user.is_phone_verified

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["email"] = self.user.email
        data["phone_number"] = self.user.phone_number
        data["is_email_verified"] = self.user.is_email_verified
        data["is_phone_verified"] = self.user.is_phone_verified

        return data


class SlidingTokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    refresh = serializers.CharField(required=False)


class SlidingRefreshResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class SlidingTokenRequestSerializer(TokenObtainSlidingSerializer):
    pass


class SlidingRefreshRequestSerializer(TokenRefreshSlidingSerializer):
    pass

class GoogleLoginInputSerializer(serializers.Serializer):
    id_token = serializers.CharField(help_text="The JWT ID Token returned by Google Sign-In.")


class FacebookLoginInputSerializer(serializers.Serializer):
    access_token = serializers.CharField(help_text="The User Access Token returned by Facebook Login SDK.")




