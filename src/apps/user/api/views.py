from rest_framework.viewsets import ModelViewSet

from apps.user import models
from apps.user.api import serializers
from apps.utils.permissions import IsSupperUser


class UserViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ['username']
    permission_classes = [
        IsSupperUser
    ]
