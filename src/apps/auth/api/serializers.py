from django.contrib.auth.models import Permission
from rest_framework import serializers

from apps.user.models import User


class EmptySerializer(serializers.Serializer):
    """An empty serializer for views that do not require input/output"""


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False)


class VerifyOtpSerializer(serializers.ModelSerializer):
    otp_session = serializers.UUIDField()

    class Meta:
        model = User
        fields = ["otp_secret", "otp_session"]


class EnableOtpSerializer(serializers.Serializer):
    otp_session = serializers.UUIDField()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["__all__"]
