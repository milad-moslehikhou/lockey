from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.credential_share.models import CredentialShare
from apps.credential_share.api.serializers import (
    CredentialShareSerializer
)


class CredentialShareViewSet(ModelViewSet):
    queryset = CredentialShare.objects.all()
    serializer_class = CredentialShareSerializer

    filterset_fields = ['shared_by', 'shared_with_user', 'shared_with_group', 'shared_with_team']
    search_fields = ['credential']
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissions
    ]
