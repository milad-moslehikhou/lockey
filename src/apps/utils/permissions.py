from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.whitelist.models import Whitelist


class IsSupperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class WhitelistPermission(BasePermission):
    """
    Global permission check for whitelist IPs.
    """

    def has_permission(self, request, view):
        remote_ip = request.META['REMOTE_ADDR']
        allow_user = Whitelist.objects.filter(ip=remote_ip, user=request.user).exists()
        allow_any = Whitelist.objects.filter(ip=remote_ip).exists()
        return allow_any or allow_user


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user
