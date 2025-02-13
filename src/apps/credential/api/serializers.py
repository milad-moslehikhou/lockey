from rest_framework import serializers

from apps.credential.models import (
    Credential,
    CredentialFavorite,
    CredentialGrant,
    CredentialSecret,
    CredentialShare,
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


class CredentialSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField()

    class Meta:
        model = Credential
        fields = "__all__"


class CredentialModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"


class CredentialShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialShare
        fields = "__all__"
