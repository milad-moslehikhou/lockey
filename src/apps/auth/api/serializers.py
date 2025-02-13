from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["__all__"]


class EmptySerializer(serializers.Serializer):
    """An empty serializer for views that do not require input/output"""
