from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        groups = data.getlist("groups[]")
        if groups:
            validated_data["groups"] = groups
        permissions = data.getlist("user_permissions[]")
        if permissions:
            validated_data["user_permissions"] = permissions
        return validated_data


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserSetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128, allow_blank=False)
    new_password2 = serializers.CharField(max_length=128, allow_blank=False)
    force_change_pass = serializers.BooleanField()


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, allow_blank=False)
    new_password1 = serializers.CharField(max_length=128, allow_blank=False)
    new_password2 = serializers.CharField(max_length=128, allow_blank=False)
