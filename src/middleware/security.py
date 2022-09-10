import os
import logging

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication

from apps.whitelist.models import Whitelist

_logger = logging.getLogger('lockey.security')


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = None
        try:
            auth = TokenAuthentication()
            user, _ = auth.authenticate(request=request)
        except TypeError:
            pass

        request.user = user or AnonymousUser()
        response = self.get_response(request)
        return response


class AuditLogMiddleware:
    """
    Audit log for all requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.user.username if request.user.username else 'anonymous'
        response = self.get_response(request)

        _logger.info('{}@{} "{} {}" {}'.format(
            username,
            request.META["REMOTE_ADDR"],
            request.method,
            request.get_full_path(),
            response.status_code
        )
        )
        return response


class AccessWhitelistMiddleware:
    """
    General white list security check.
    """

    _message = "Access denied, you are not in the white list."

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not os.getenv('LOCKEY_ENABLE_WHITELIST', True):
            _logger.debug(
                "Access whitelist currently is disabled, for enable there set LOCKEY_ENABLE_WHITELIST to True"
            )
            return self.get_response(request)

        remote_ip = request.META['REMOTE_ADDR']
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            user = request.user
            if Whitelist.objects.filter(
                Q(ip=remote_ip, user=user) | Q(ip=remote_ip, user=None)
            ).exists():
                return self.get_response(request)
            else:
                return HttpResponseForbidden()
        else:
            if Whitelist.objects.filter(ip=remote_ip, user=None).exists():
                return self.get_response(request)
            else:
                return HttpResponseForbidden()
