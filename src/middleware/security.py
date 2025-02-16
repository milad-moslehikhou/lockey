import json
import logging
from datetime import timedelta

import environ
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone
from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.whitelist.models import Whitelist

_logger = logging.getLogger("lockey.security")


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
        username = request.user.username if request.user.username else "anonymous"
        response = self.get_response(request)
        client_ip = request.META.get("REMOTE_ADDR")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0]

        _logger.info(f'{username}@{client_ip} "{request.method} {request.get_full_path()}" {response.status_code}')
        return response


class AccessWhitelistMiddleware:
    """
    General white list security check.
    """

    _message = "Access denied, you are not in the white list."

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        env = environ.Env()
        if env.bool("LOCKEY_ENABLE_WHITELIST", True):
            _logger.debug("Access whitelist currently is disabled, for enable there set LOCKEY_ENABLE_WHITELIST=true")
            return self.get_response(request)

        client_ip = request.META.get("REMOTE_ADDR")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0]
        error = {
            "type": "client_error",
            "errors": [{"detail": "You are not allowed to reach the resources. Please contact administrator."}],
        }
        if hasattr(request, "user") and not isinstance(request.user, AnonymousUser):
            user = request.user
            if Whitelist.objects.filter(Q(ip=client_ip, user=user) | Q(ip=client_ip, user=None)).exists():
                return self.get_response(request)
            else:
                return HttpResponseForbidden(content=json.dumps(error))
        elif Whitelist.objects.filter(ip=client_ip, user=None).exists():
            return self.get_response(request)
        else:
            return HttpResponseForbidden(content=json.dumps(error))


class PasswordExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expiration_days = timedelta(days=getattr(settings, "PASSWORD_EXPIRATION_DAYS", 90.0))

    def __call__(self, request):
        resolve_match = resolve(request.path)
        if resolve_match.app_name == "admin" and request.user.is_authenticated:
            latest_record = request.user.password_records.latest()
            if (timezone.now() - latest_record.date) >= self.expiration_days:
                if resolve_match.url_name != "password_change":
                    return redirect(reverse("admin:password_change", current_app=resolve_match.namespace))
                if request.method == "GET":
                    messages.warning(
                        request,
                        (
                            f"It has exceeded {self.expiration_days.days} and the password cannot be changed. "
                            "Please change it before continuing."
                        ),
                        fail_silently=True,
                    )

        response = self.get_response(request)
        return response
