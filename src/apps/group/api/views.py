from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet

from apps.group.api.serializers import GroupSerializer
from apps.utils.permissions import WhitelistPermission, IsSupperUser


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    filterset_fields = None
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']

    permission_classes = [
        WhitelistPermission,
        IsSupperUser
    ]
