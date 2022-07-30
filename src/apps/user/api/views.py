from rest_framework.viewsets import ModelViewSet

from ..models import User
from .serializers import UserSerializer
from apps.utils.permissions import IsSupperUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    permission_classes = [
        IsSupperUser
    ]
