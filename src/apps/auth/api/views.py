from django.contrib.auth.signals import user_logged_in
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import EmptySerializer


@extend_schema(tags=["Auth"])
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        request.user = user
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return super(LoginView, self).post(request, format=None)


@extend_schema(tags=["Auth"], responses={204: None})
class LogoutView(KnoxLogoutView):
    serializer_class = EmptySerializer


@extend_schema(tags=["Auth"], responses={204: None})
class LogoutAllView(KnoxLogoutAllView):
    serializer_class = EmptySerializer
