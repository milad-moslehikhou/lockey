from rest_framework import serializers

from apps.credential import models


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Credential
        fields = '__all__'


class CredentialSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CredentialSecret
        fields = '__all__'


class CredentialGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CredentialGrant
        fields = '__all__'


class CredentialShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CredentialShare
        fields = '__all__'
