from django.contrib.auth.models import Permission
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.permission.api.serializers import PermissionSerializer
from utils.permissions import IsSupperUser


@extend_schema(tags=["Permission"])
class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    filterset_fields = None
    search_fields = ["name", "codename"]
    ordering_fields = ["id", "name", "codename"]
    ordering = ["-id"]

    permission_classes = [IsSupperUser]
