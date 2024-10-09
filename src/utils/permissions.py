from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.credential.models import CredentialGrant


class IsSupperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    message = _("Object is read-only")

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        """

        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user


class UserHasAccessGrantOnCredential(BasePermission):
    """
    Allow access to users who have grant on credential object.
    """

    message = _("You don't have enough grant on this credential")

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in ('HEAD', 'OPTIONS') or user.is_superuser:
            return True
        if request.method == 'GET':
            return CredentialGrant.objects.filter(
                Q(credential=obj) &
                (Q(team=user.team) | Q(group__in=user.groups.all()) | Q(user=user))
            ).exists()
        return CredentialGrant.objects.filter(
            Q(credential=obj) &
            Q(action=CredentialGrant.Action.MODIFY) &
            (Q(team=user.team) | Q(group__in=user.groups.all()) | Q(user=user))
        ).exists()
