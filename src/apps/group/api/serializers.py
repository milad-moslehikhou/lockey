from django.contrib.auth.models import Group

from rest_framework import serializers

from apps.user.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupModifySerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.ModelField(User()._meta.get_field('id')))

    class Meta:
        model = Group
        fields = '__all__'


class GroupMemberSerializer(serializers.Serializer):
    members = serializers.ListField(child=serializers.ModelField(User()._meta.get_field('id')))
