from rest_framework.viewsets import ModelViewSet

from apps.user.models import User
from apps.user.api.serializers import UserSerializer
from apps.utils.permissions import WhitelistPermission, IsSupperUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    permission_classes = [
        WhitelistPermission,
        IsSupperUser
    ]
