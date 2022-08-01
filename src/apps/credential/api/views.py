from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, DjangoModelPermissions

from apps.utils.permissions import WhitelistPermission, UserHasAccessGrantOnCredential

from apps.credential.models import Credential, CredentialShare
from apps.credential.api.serializers import (
    CredentialModifySerializer,
    CredentialSerializer,
    CredentialShareSerializer
)


class CredentialViewSet(ModelViewSet):
    queryset = Credential.objects.all()

    filterset_fields = ['importancy', 'is_public', 'auto_genpass', 'team', 'created_by', 'modified_by']
    search_fields = ['name', 'username', 'ip', 'uri']
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        WhitelistPermission,
        IsAuthenticated,
        DjangoModelPermissions,
        UserHasAccessGrantOnCredential
    ]

    def get_queryset(self):
        """
        This view should return a list of all the credential
        for the currently authenticated user's team.
        """

        user = self.request.user
        if user.is_superuser:
            return Credential.objects.all()
        return Credential.objects.filter(team=user.team)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CredentialSerializer
        return CredentialModifySerializer


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
