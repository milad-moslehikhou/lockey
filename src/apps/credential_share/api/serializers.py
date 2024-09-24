from rest_framework import serializers

from apps.credential_share.models import (
    CredentialShare
)


class CredentialShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialShare
        fields = '__all__'
