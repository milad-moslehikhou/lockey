from django.db.models import Q
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.credential.models import CredentialGrant
from apps.user.api.serializers import UserSerializer
from apps.credential.api.serializers import CredentialGrantSerializer
from apps.auth.api.serializers import PermissionSerializer
from utils.permissions import IsSupperUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    permission_classes = [
        IsSupperUser
    ]

    @action(
        methods=['GET'],
        url_name="all-permissions",
        url_path="all-permissions",
        detail=True
    )
    def get_all_permissions(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        permissions = Permission.objects.filter(
            Q(user=user) | Q(group__in=user.groups.all())
        )
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        url_name="all-grants",
        url_path="all-grants",
        detail=True
    )
    def get_all_grants(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        grants = CredentialGrant.objects.filter(
            Q(user=user) | Q(team=user.team) | Q(group__in=user.groups.all())
        )
        serializer = CredentialGrantSerializer(grants, many=True)
        return Response(serializer.data)
