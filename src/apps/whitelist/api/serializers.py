from rest_framework import serializers

from ..models import Whitelist


class WhitelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whitelist
        fields = '__all__'
