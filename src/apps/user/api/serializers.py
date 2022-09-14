from rest_framework import serializers

from apps.user.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserGetSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        exclude = ['password']
