from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.models import User

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
            return Response(
                {"non_field_errors": ["Invalid username or password"]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        otp_session = user.generate_otp_session()
        if not user.otp_secret:
            return Response(otp_session, status=status.HTTP_202_ACCEPTED)
        return Response(otp_session, status=status.HTTP_200_OK)


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
        otp_secret = serializer.validated_data["otp_secret"]
        otp_session = serializer.validated_data["otp_session"]
        user_id = cache.get(otp_session)
        if not user_id:
            return Response({"non_field_errors": ["Login first"]}, status=status.HTTP_400_BAD_REQUEST)

        user: User = get_object_or_404(User, pk=user_id)
        request.user = user
        if user.otp_secret:
            if user.verify_otp(otp_secret):
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
            return Response({"non_field_errors": ["Invalid OTP"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"non_field_errors": ["Two factore authentication is required"]}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(tags=["Auth"])
class EnableOtpView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EnableOtpSerializer

    def post(self, request, _format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_session = serializer.validated_data["otp_session"]
        user_id = cache.get(otp_session)
        if not user_id:
            return Response({"non_field_errors": ["Login first"]}, status=status.HTTP_400_BAD_REQUEST)
        user: User = get_object_or_404(User, pk=user_id)
        otp_secret = user.generate_otp_secret()
        otp_uri = user.get_otp_provisioning_uri()
        return Response({"otp_secret": otp_secret, "otp_uri": otp_uri})


@extend_schema(tags=["Auth"])
class RefreshTokenView(TokenRefreshView):
    pass
