from django.contrib.auth.models import Permission
from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """An empty serializer for views that do not require input/output"""


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False)


class VerifyOtpSerializer(serializers.Serializer):
    otp_session = serializers.UUIDField()
    otp_code = serializers.CharField(min_length=6, max_length=6)


class EnableOtpSerializer(serializers.Serializer):
    otp_session = serializers.UUIDField()
    regenerate = serializers.BooleanField(default=False)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["__all__"]
