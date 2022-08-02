from django.contrib.auth import login

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView)

from apps.utils.permissions import WhitelistPermission


class LoginView(KnoxLoginView):
    permission_classes = [
        WhitelistPermission
    ]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(KnoxLogoutView):
    permission_classes = [
        WhitelistPermission,
        IsAuthenticated
    ]


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = [
        WhitelistPermission,
        IsAuthenticated
    ]
