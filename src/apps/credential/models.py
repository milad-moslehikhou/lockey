from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from apps.folder.models import Folder
from apps.user.models import User


class Credential(models.Model):
    class Importancy(models.TextChoices):
        HIGH = "HIGH", _("High")
        MEDIUM = "MEDIUM", _("Medium")
        LOW = "LOW", _("Low")

    name = models.CharField(verbose_name=_("name"), max_length=150)
    username = models.CharField(verbose_name=_("username"), max_length=150)
    ip = models.CharField(verbose_name=_("ip address"), max_length=15, blank=True)
    uri = models.URLField(verbose_name=_("uri"), blank=True)
    importancy = models.CharField(
        verbose_name=_("importancy"), max_length=8, choices=Importancy.choices, default=Importancy.LOW
    )
    auto_genpass = models.BooleanField(verbose_name=_("auto generate"), default=False)
    tags = models.CharField(verbose_name=_("tags"), max_length=255, blank=True)
    description = models.CharField(verbose_name=_("description"), max_length=255, blank=True)
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        verbose_name=_("folder"),
        related_name="credentials",
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column="created_by",
        verbose_name=_("created by"),
        related_name="created_credentials",
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column="modified_by",
        verbose_name=_("modified by"),
        related_name="modified_credentials",
    )
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)

    class Meta:
        permissions = (("add_public_credential", "Can add public credential"),)

    def __str__(self):
        return f"{self.username}@{self.name}"


class CredentialSecret(models.Model):
    password = encrypt(models.CharField(verbose_name=_("password"), max_length=150))
    expire_at = models.DateTimeField(verbose_name=_("expire at"))
    category = models.TextField(verbose_name=_("category"), max_length=36, blank=True)
    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="secrets",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        verbose_name=_("created by"),
        related_name="created_secrets",
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.credential} {self.category} {self.expire_at}"


class CredentialFavorite(models.Model):
    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="credential_favorites",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(name="uq__credential__user", fields=["credential", "user"]),
        ]

    def __str__(self):
        return f"{self.user} {self.credential}"


class CredentialGrant(models.Model):
    class Action(models.TextChoices):
        VIEW = "VIEW", _("View")
        MODIFY = "MODIFY", _("Modify")

    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="grants",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grants", null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="grants", null=True)
    action = models.CharField(verbose_name=_("action"), max_length=150, choices=Action.choices, default=Action.VIEW)
    until = models.DateTimeField(verbose_name=_("granted until"), null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="uq__credential__action__user", fields=["credential", "action", "user"]),
            models.UniqueConstraint(name="uq__credential__action__group", fields=["credential", "action", "group"]),
        ]

    def __str__(self):
        return f"{self.group} {self.user} {self.credential} {self.action}"


class CredentialGrantRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SENT = "SENT", _("Sent")
        DONE = "DONE", _("Done")

    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="grant_requests",
    )

    secret = models.CharField(
        verbose_name=_("secret"),
        max_length=320,
        blank=False,
    )
    requester = models.ForeignKey(
        User,
        related_name="grant_requests",
        on_delete=models.CASCADE,
        verbose_name=_("requester"),
    )
    respondent = models.ForeignKey(
        User,
        related_name="grant_response",
        on_delete=models.CASCADE,
        verbose_name=_("respondent"),
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )

    def __str__(self):
        return self.request_string

    @property
    def request_string(self):
        return f"{self.requester}:{self.credential}:{self.secret}"
