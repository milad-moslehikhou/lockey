from django.db.models import Q
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.serializers import ValidationError, DjangoValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User, PasswordRecord
from apps.credential.models import CredentialGrant
from apps.user.api.serializers import (
    UserSerializer,
    UserGetSerializer,
    UserSetPasswordSerializer,
    UserChangePasswordSerializer
    )
from apps.credential.api.serializers import CredentialGrantSerializer
from apps.auth.api.serializers import PermissionSerializer
from utils.permissions import IsSupperUser, SAFE_METHODS


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filterset_fields = ['username']
    permission_classes = [
        IsSupperUser
    ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserGetSerializer
        return UserSerializer

    def get_permissions(self):
        if self.get_view_name() == "Change userpassword":
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

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
            Q(user=user) | Q(group__in=user.groups.all())
        )
        serializer = CredentialGrantSerializer(grants, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        url_name='set-password',
        url_path='set-password',
        detail=True
    )
    def set_userpassword(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password1 = serializer.validated_data.pop('new_password1')
        new_password2 = serializer.validated_data.pop('new_password2')
        force_change_pass = serializer.validated_data.pop('force_change_pass', True)
        if new_password1 != new_password2:
            raise ValidationError({'new_password2': 'Password do not match.'})
        user.set_password(new_password1)
        user.force_change_pass = force_change_pass
        user.save()
        passRecord = PasswordRecord(user=user, password=user.password)
        passRecord.save()
        return Response(status=status.HTTP_200_OK)

    @action(
            methods=['POST'],
            url_name='change-password',
            url_path='change-password',
            detail=True
    )
    def change_userpassword(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.pop('old_password')
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Incorrect password.'})
        new_password1 = serializer.validated_data.pop('new_password1')
        try:
            validate_password(new_password1, user)
        except DjangoValidationError as e:
            raise ValidationError({'new_password1': '\n'.join(e)})
        new_password2 = serializer.validated_data.pop('new_password2')
        if new_password1 != new_password2:
            raise ValidationError({'new_password2': 'Password do not match.'})
        user.set_password(new_password1)
        user.force_change_pass = False
        user.save()
        passRecord = PasswordRecord(user=user, password=user.password)
        passRecord.save()
        return Response(status=status.HTTP_200_OK)
