from django.db.models import Q, Case, When, Value, FilteredRelation
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status

from utils.permissions import UserHasAccessGrantOnCredential

from apps.credential.models import Credential, CredentialFavorite, CredentialShare
from apps.credential.api.serializers import (
    CredentialModifySerializer,
    CredentialSerializer,
    CredentialShareSerializer
)


class CredentialViewSet(ModelViewSet):
    filterset_fields = ['importancy', 'is_public', 'auto_genpass', 'folder', 'team', 'created_by', 'modified_by']
    search_fields = ['name', 'username', 'ip', 'uri']
    ordering_fields = '__all__'
    ordering = ['-id']

    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissions,
        UserHasAccessGrantOnCredential
    ]

    def get_queryset(self):
        """
        This view should return a list of all the credential
        for the currently authenticated user.
        """
        if self.request.method in SAFE_METHODS:
            user = self.request.user
            return Credential.objects.filter(
                (Q(team=user.team) & Q(is_public=True)) | Q(created_by=user)
            ).annotate(favorite=FilteredRelation(
                'favorites', condition=Q(favorites__user=user)
            )
            ).annotate(is_favorite=Case(
                When(favorites__user=user, then=Value(False)),
                default=Value(True)
            )
            )

        return Credential.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CredentialSerializer
        return CredentialModifySerializer

    @action(
        methods=['POST', 'DELETE'],
        url_name="favorite",
        url_path="favorite",
        detail=True
    )
    def favorite(self, request, pk=None):
        user = request.user
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == 'POST':
            favorite = CredentialFavorite(user=user, credential=credential)
            favorite.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'DELETE':
            favorite = get_object_or_404(CredentialFavorite, user=user, credential=credential)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
