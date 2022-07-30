from rest_framework.viewsets import ModelViewSet

from ..models import Whitelist
from .serializers import WhitelistSerializer
from apps.utils.permissions import IsSupperUser


class WhitelistViewSet(ModelViewSet):
    queryset = Whitelist.objects.all()
    serializer_class = WhitelistSerializer

    filterset_fields = ['ip', 'user']
    search_fields = ['ip', 'user']
    ordering_fields = ['id', 'ip', 'user']
    ordering = ['-id']

    permission_classes = [
        IsSupperUser
    ]
