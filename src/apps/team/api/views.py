from rest_framework.viewsets import ModelViewSet

from apps.team.models import Team
from apps.team.api.serializers import TeamSerializer
from apps.utils.permissions import WhitelistPermission, IsSupperUser


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    filterset_fields = ['groups']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']

    permission_classes = [
        WhitelistPermission,
        IsSupperUser
    ]
