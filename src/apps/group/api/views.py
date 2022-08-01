from django.contrib.auth import models

from rest_framework.viewsets import ModelViewSet

from apps.group.api.serializers import GroupSerializer
from apps.utils.permissions import IsSupperUser


class GroupViewSet(ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = GroupSerializer

    filterset_fields = None
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']

    permission_classes = [
        IsSupperUser
    ]
