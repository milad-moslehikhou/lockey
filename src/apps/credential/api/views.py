from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.credential import models
from apps.credential.api import serializers


class CredentialCategoryViewSet(ModelViewSet):
    queryset = models.CredentialCategory.objects.all()
    serializer_class = serializers.CredentialCategorySerializer

    filterset_fields = ['is_public', 'parent', 'team', 'user']
    search_fields = None
    ordering_fields = None

    permission_classes = [
        IsAuthenticated
    ]


class CredentialViewSet(ModelViewSet):
    queryset = models.Credential.objects.all()
    serializer_class = serializers.CredentialSerializer

    filterset_fields = ['importancy', 'is_public', 'auto_genpass', 'team', 'category', 'created_by', 'modified_by']
    search_fields = ['name', 'username', 'ip', 'uri']
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated
    ]


class CredentialSecretViewSet(ModelViewSet):
    queryset = models.CredentialSecret.objects.all()
    serializer_class = serializers.CredentialSecretSerializer

    filterset_fields = ['credential', 'created_by']
    search_fields = None
    ordering_fields = None

    permission_classes = [
        IsAuthenticated
    ]


class CredentialGrantViewSet(ModelViewSet):
    queryset = models.CredentialGrant.objects.all()
    serializer_class = serializers.CredentialGrantSerializer

    filterset_fields = ['credential', 'user', 'group', 'team', 'action']
    search_fields = None
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated
    ]


class CredentialShareViewSet(ModelViewSet):
    queryset = models.CredentialShare.objects.all()
    serializer_class = serializers.CredentialShareSerializer

    filterset_fields = ['shared_by', 'shared_with_user', 'shared_with_group', 'shared_with_team']
    search_fields = ['credential']
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated
    ]
