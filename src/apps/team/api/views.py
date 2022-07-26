from rest_framework.viewsets import ModelViewSet

from apps.team import models
from apps.team.api import serializers
from apps.utils.permissions import IsSupperUser


class TeamViewSet(ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    filterset_fields = ['groups']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']

    permission_classes = [
        IsSupperUser
    ]
