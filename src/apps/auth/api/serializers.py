from django.contrib.auth.models import Permission
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["__all__"]


class EmptySerializer(serializers.Serializer):
    """An empty serializer for views that do not require input/output"""


class VerifyOtpSerializer(AuthTokenSerializer):
    otp = serializers.CharField(max_length=6, allow_blank=False)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False)
