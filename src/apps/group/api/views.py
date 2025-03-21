from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.group.api.serializers import GroupMemberSerializer, GroupModifySerializer, GroupSerializer
from apps.user.api.serializers import UserGetSerializer
from apps.user.models import User
from utils.permissions import SAFE_METHODS, IsSupperUser


@extend_schema(tags=["Group"])
class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    filterset_fields = None
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    ordering = ["-id"]

    permission_classes = [IsSupperUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = GroupModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        members = serializer.validated_data.pop("members")
        group = serializer.save()
        group.user_set.add(*members)
        group.save()
        group_serializer = GroupSerializer(group)
        headers = self.get_success_headers(data=group_serializer.data)
        return Response(status=status.HTTP_201_CREATED, data=group_serializer.data, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = GroupModifySerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        members = serializer.validated_data.pop("members")
        instance.user_set.clear()
        instance.user_set.add(*members)
        instance.save()
        group_serializer = GroupSerializer(instance)
        headers = self.get_success_headers(data=group_serializer.data)
        return Response(status=status.HTTP_200_OK, data=group_serializer.data, headers=headers)

    @action(methods=["GET", "PATCH"], url_name="members", url_path="members", detail=True)
    def get_group_members(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        if request.method == "GET":
            members = group.user_set.all()
            serializer = UserGetSerializer(members, many=True)
            return Response(data=serializer.data)
        if request.method == "PATCH":
            serializer = GroupMemberSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            members = serializer.validated_data.pop("members")
            group.user_set.clear()
            for member in members:
                user = get_object_or_404(User, pk=member)
                group.user_set.add(user)
            group.save()
            return Response(status=status.HTTP_200_OK)
