from django.contrib.auth import login, logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView)


class LoginView(KnoxLoginView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(KnoxLogoutView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, format=None):
        request._auth.delete()
        logout(request=request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        logout(request=request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
