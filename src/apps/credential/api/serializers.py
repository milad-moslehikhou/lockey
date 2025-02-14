from rest_framework import serializers

from apps.credential.models import (
    Credential,
    CredentialFavorite,
    CredentialGrant,
    CredentialGrantRequest,
    CredentialSecret,
)


class CredentialSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialSecret
        fields = "__all__"


class CredentialFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialFavorite
        fields = "__all__"


class CredentialGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialGrant
        fields = "__all__"


class CredentialGrantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialGrantRequest
        fields = ["respondent"]


class CredentialSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField()

    class Meta:
        model = Credential
        fields = "__all__"


class CredentialModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"
