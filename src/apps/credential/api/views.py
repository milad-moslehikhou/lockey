from django.db.models import Q, Case, When, Value, FilteredRelation
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status

from utils.permissions import UserHasAccessGrantOnCredential

from apps.credential.models import Credential, CredentialFavorite, CredentialShare, CredentialSecret
from apps.credential.api.serializers import (
    CredentialModifySerializer,
    CredentialSerializer,
    CredentialShareSerializer,
    CredentialSecretSerializer,
)


class CredentialViewSet(ModelViewSet):
    filterset_fields = ['importancy', 'is_public', 'auto_genpass', 'folder', 'created_by', 'modified_by']
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
                (Q(is_public=True)) | Q(created_by=user)
            ).annotate(favorite=FilteredRelation(
                'favorites', condition=Q(favorites__user=user)
            )
            ).annotate(is_favorite=Case(
                When(favorite__isnull=True, then=Value(False)),
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

    @action(
        methods=['GET', 'PATCH'],
        url_name='share',
        url_path='share',
        detail=True
    )
    def share(self, request, pk=None):
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == 'GET':
            shares = credential.share_with.all()
            serializer = CredentialShareSerializer(shares, many=True)
            return Response(serializer.data)
        if request.method == 'PATCH':
            credential.share_with.all().delete()
            serializer = CredentialShareSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @action(
        methods=['GET'],
        url_name='all-shared',
        url_path='all-shared',
        detail=False
    )
    def get_all_shared(self, request):
        shares = CredentialShare.objects.all()
        serializer = CredentialShareSerializer(shares, many=True)
        return Response(serializer.data)

    @action(
        methods=['GET', 'POST'],
        url_name='secret',
        url_path='secret',
        detail=True
    )
    def get_secret(self, request, pk=None):
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == 'GET':
            secret = CredentialSecret.objects.filter(credential=credential).order_by('-id')[:2]
            serializer = CredentialSecretSerializer(secret, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = CredentialSecretSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
