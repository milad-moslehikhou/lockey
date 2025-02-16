import pyotp
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.models import User

from .serializers import EmptySerializer, LoginSerializer, VerifyOtpSerializer


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
        if not user.otp_secret:
            return Response({"data": "2FA is required"}, status=status.HTTP_202_ACCEPTED)
        return Response({"user_id": user.id}, status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"], responses={204: None})
class LogoutView(KnoxLogoutView):
    serializer_class = EmptySerializer


@extend_schema(tags=["Auth"], responses={204: None})
class LogoutAllView(KnoxLogoutAllView):
    serializer_class = EmptySerializer


@extend_schema(tags=["Auth"])
class VerifyOtpView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifyOtpSerializer

    def post(self, request, _format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]
        request.user = user
        if user.otp_secret:
            totp = pyotp.TOTP(user.otp_secret)
            if totp.verify(otp):
                return super().post(request, format=None)
            return Response({"non_field_errors": ["Invalid OTP"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"non_field_errors": ["2FA is required"]}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class EnableOtpView(APIView):
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
        user.otp_secret = pyotp.random_base32()
        user.save()
        uri = pyotp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name="Lockey")
        return Response({"secret": user.otp_secret, "uri": uri})
