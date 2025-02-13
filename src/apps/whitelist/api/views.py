from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.whitelist.api.serializers import WhitelistSerializer
from apps.whitelist.models import Whitelist
from utils.permissions import IsSupperUser


@extend_schema(tags=["Whitelist"])
class WhitelistViewSet(ModelViewSet):
    queryset = Whitelist.objects.all()
    serializer_class = WhitelistSerializer

    filterset_fields = ["ip", "user"]
    search_fields = ["ip", "user"]
    ordering_fields = ["id", "ip", "user"]
    ordering = ["-id"]

    permission_classes = [IsSupperUser]
