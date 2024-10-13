import os
import logging
import json
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse, resolve
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

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
        except (TypeError, AuthenticationFailed):
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
        error = {
                    'type': "client_error",
                    'errors': [{'detail': "You are not allowed to reach the resources. Please contact administrator."}]
                }
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            user = request.user
            if Whitelist.objects.filter(
                Q(ip=remote_ip, user=user) | Q(ip=remote_ip, user=None)
            ).exists():
                return self.get_response(request)
            else:
                return HttpResponseForbidden(content=json.dumps(error))
        else:
            if Whitelist.objects.filter(ip=remote_ip, user=None).exists():
                return self.get_response(request)
            else:
                return HttpResponseForbidden(content=json.dumps(error))


class PasswordExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expiration_days = timedelta(
            days=getattr(settings, 'PASSWORD_EXPIRATION_DAYS', 90.0)
        )

    def __call__(self, request):
        resolve_match = resolve(request.path)
        if resolve_match.app_name == 'admin' and request.user.is_authenticated:
            latest_record = request.user.password_records.latest()
            if (timezone.now() - latest_record.date) >= self.expiration_days:
                if resolve_match.url_name != 'password_change':
                    return redirect(reverse(
                        "admin:password_change",
                        current_app=resolve_match.namespace
                    ))
                if request.method == 'GET':
                    messages.warning(
                        request,
                        'It has exceeded {} and the password cannot be changed. Please change it before continuing.'.
                        format(
                            self.expiration_days.days
                        ),
                        fail_silently=True,
                    )

        response = self.get_response(request)
        return response
