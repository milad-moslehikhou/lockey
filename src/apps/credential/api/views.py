import secrets

from django.db.models import Case, FilteredRelation, Q, Value, When
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import ModelViewSet

from apps.credential.api.serializers import (
    CredentialGrantRequestSerializer,
    CredentialGrantResponseSerializer,
    CredentialGrantSerializer,
    CredentialModifySerializer,
    CredentialSecretSerializer,
    CredentialSerializer,
)
from apps.credential.models import (
    Credential,
    CredentialFavorite,
    CredentialGrant,
    CredentialGrantRequest,
    CredentialSecret,
)
from apps.user.models import User
from utils.permissions import CredentialGrantPermission


@extend_schema(tags=["Credential"])
class CredentialViewSet(ModelViewSet):
    filterset_fields = ["importancy", "auto_genpass", "folder", "created_by", "modified_by"]
    search_fields = ["name", "username", "ip", "uri"]
    ordering_fields = "__all__"

    permission_classes = [IsAuthenticated, DjangoModelPermissions, CredentialGrantPermission]

    def get_queryset(self):
        """
        This view should return a list of all the credential
        for the currently authenticated user.
        """
        if getattr(self, "swagger_fake_view", False):
            return Credential.objects.none()

        if self.request.method in SAFE_METHODS:
            user = self.request.user
            return (
                Credential.objects.filter(
                    Q(created_by=user) | Q(grants__user=user) | Q(grants__group__in=user.groups.all())
                )
                .annotate(favorite=FilteredRelation("favorites", condition=Q(favorites__user=user)))
                .annotate(is_favorite=Case(When(favorite__isnull=True, then=Value(False)), default=Value(True)))
            )

        return Credential.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CredentialSerializer
        return CredentialModifySerializer

    @action(methods=["POST", "DELETE"], url_name="favorite", url_path="favorite", detail=True)
    def favorite(self, request, pk: int | None = None):
        user = request.user
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == "POST":
            favorite = CredentialFavorite(user=user, credential=credential)
            favorite.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == "DELETE":
            favorite = get_object_or_404(CredentialFavorite, user=user, credential=credential)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET", "PATCH"], url_name="grant", url_path="grant", detail=True)
    def grant(self, request, pk: int | None = None):
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == "GET":
            grants = credential.grants.all()
            serializer = CredentialGrantSerializer(grants, many=True)
            return Response(serializer.data)
        if request.method == "PATCH":
            credential.grants.all().delete()
            serializer = CredentialGrantSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["POST"], url_name="grant-request", url_path="grant-request", detail=True)
    def grant_request(self, request, pk: int | None = None):
        credential = get_object_or_404(Credential, pk=pk)
        user: User = request.user
        serializer = CredentialGrantRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        respondent = serializer.validated_data.get("respondent")
        random_secret = secrets.token_hex(8)
        CredentialGrantRequest(
            credential=credential,
            requester=user,
            respondent=respondent,
            secret=random_secret,
        ).save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["POST"], url_name="grant-response", url_path="grant-response", detail=False)
    def grant_response(self, request):
        serializer = CredentialGrantResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_string = serializer.validated_data.get("response_string")
        sender = serializer.validated_data.get("sender")
        pk = response_string.split(":")[0]
        grant_request = get_object_or_404(CredentialGrantRequest, pk=pk)
        if grant_request.respondent == sender and grant_request.request_string == response_string:
            grant_request.status = CredentialGrantRequest.Status.DONE
            grant_request.save()
            CredentialGrant(
                credential=grant_request.credential,
                user=grant_request.requester,
            ).save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET", "POST"], url_name="secret", url_path="secret", detail=True)
    def secret(self, request, pk: int | None = None):
        credential = get_object_or_404(Credential, pk=pk)
        if request.method == "GET":
            secret = CredentialSecret.objects.filter(credential=credential).order_by("-id")[:2]
            serializer = CredentialSecretSerializer(secret, many=True)
            return Response(serializer.data)
        if request.method == "POST":
            serializer = CredentialSecretSerializer(data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save(credential=credential)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data, headers=headers)
