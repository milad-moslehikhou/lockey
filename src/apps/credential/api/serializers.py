from rest_framework import serializers

from apps.credential.models import (
    Credential,
    CredentialSecret,
    CredentialGrant,
    CredentialShare
)


class CredentialSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialSecret
        fields = '__all__'


class CredentialGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialGrant
        fields = '__all__'


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class CredentialModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'

    secrets = CredentialSecretSerializer(many=True)
    grants = CredentialGrantSerializer(many=True)


class CredentialShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialShare
        fields = '__all__'
