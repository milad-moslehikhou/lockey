from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.api.serializers import UserGetSerializer
from apps.user.models import User
from utils.responses import ClientErrorResponse

from .serializers import EmptySerializer, EnableOtpSerializer, LoginSerializer, VerifyOtpSerializer


@extend_schema(tags=["Auth"])
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, _format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user: User = authenticate(request, username=username, password=password)
        if not user:
            return ClientErrorResponse("Invalid username or password", status.HTTP_401_UNAUTHORIZED)
        serializer = UserGetSerializer(user)
        otp_session = user.generate_otp_session()
        content = {"user": serializer.data, "otp_session": otp_session}
        if not user.otp_secret:
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(content, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"], responses={204: None})
class LogoutView(APIView):
    serializer_class = EmptySerializer

    def post(self, request):
        logout(request)
        return Response({"data": "User logged out"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Auth"])
class VerifyOtpView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifyOtpSerializer

    def post(self, request, _format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data["otp_code"]
        otp_session = serializer.validated_data["otp_session"]
        user_id = cache.get(otp_session)
        if not user_id:
            return ClientErrorResponse("Login first", status.HTTP_400_BAD_REQUEST)

        user: User = get_object_or_404(User, pk=user_id)
        request.user = user
        if user.otp_secret:
            if user.verify_otp(otp_code):
                login(request, user)
                refresh, access = user.generate_tokens()
                response = Response({"access_token": access}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=settings.PRODUCTION,
                    samesite="Lax",
                    max_age=3600,
                )
                return response
            return ClientErrorResponse("Two-factore authentication code is invalid", status.HTTP_401_UNAUTHORIZED)
        return ClientErrorResponse("Two-factore authentication is required", status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class EnableOtpView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EnableOtpSerializer

    def post(self, request, _format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_session = serializer.validated_data["otp_session"]
        regenerate = serializer.validated_data["regenerate"]
        user_id = cache.get(otp_session)
        if not user_id:
            return ClientErrorResponse("Login first!", status=status.HTTP_400_BAD_REQUEST)
        user: User = get_object_or_404(User, pk=user_id)
        otp_secret = user.otp_secret
        if user.otp_secret == "" or regenerate:
            otp_secret = user.generate_otp_secret()
        otp_uri = user.get_otp_provisioning_uri()
        return Response({"otp_secret": otp_secret, "otp_uri": otp_uri})


@extend_schema(tags=["Auth"])
class RefreshTokenView(TokenRefreshView):
    pass
