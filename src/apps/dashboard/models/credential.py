from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

from .team import Team


class CredentialCategory(models.Model):
    class Meta:
        permissions = (
            ("add_public_category", "Can add public credential category"),
        )

    class Icon(models.TextChoices):
        DEFAULT = 'default.ico', _("default")
        SERVER = 'server.ico', _("server")
        LINUX_SERVER = 'linux_server.ico', _("linux server")
        WINDOWS_SERVER = 'windows_server.ico', _("windows server")
        DATABASE = 'database.ico', _("database")
        FIREWALL = 'firewall.ico', _("firewall")

    name = models.CharField(
        verbose_name=_("name"),
        max_length=150
    )
    icon = models.CharField(
        verbose_name=_("icon"),
        max_length=150,
        choices=Icon.choices,
        default=Icon.DEFAULT
    )
    color = models.CharField(
        verbose_name=_("color hex"),
        max_length=7,
        default='#ffffff'
    )
    is_public = models.BooleanField(
        verbose_name=_("is public?"),
        default=False
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True
    )


class Credential(models.Model):
    class Meta:
        permissions = (
            ("add_public_credential", "Can add public credential"),
        )

    class Importancy(models.TextChoices):
        HIGH = 'HIGH', _("High")
        MEDUIM = 'MEDUIM', _("Meduim")
        LOW = 'LOW', _("Low")

    username = models.CharField(
        verbose_name=_("username"),
        max_length=150
    )
    hostname = models.CharField(
        verbose_name=_("hostname"),
        max_length=150
    )
    ip = models.CharField(
        verbose_name=_("ip address"),
        max_length=15,
        null=True,
        blank=True
    )
    uri = models.URLField(
        verbose_name=_("uri"),
        null=True,
        blank=True
    )
    importancy = models.CharField(
        verbose_name=_("importancy"),
        max_length=150,
        choices=Importancy.choices,
        default=Importancy.LOW
    )
    is_public = models.BooleanField(
        verbose_name=_("is public?"),
        default=False
    )
    auto_genpass = models.BooleanField(
        verbose_name=_("auto generate password"),
        default=False
    )
    tags = models.CharField(
        verbose_name=_("tags"),
        max_length=255,
        null=True,
        blank=True
    )
    description = models.CharField(
        verbose_name=_("description"),
        max_length=255
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        verbose_name=_("created by"),
        related_name="created_credentials",
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="modified_by",
        verbose_name=_("modified by"),
        related_name="modified_credentials"
    )
    modified_at = models.DateTimeField(
        verbose_name=_("modified at"),
        auto_now=True
    )
    category = models.ForeignKey(
        CredentialCategory,
        on_delete=models.CASCADE,
        related_name="credentials",
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )


class CredentialSecret(models.Model):
    password = models.CharField(
        verbose_name=_("password"),
        max_length=150
    )
    expire_at = models.DateTimeField(
        verbose_name=_("expire at")
    )
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
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )


class CredentialGrant(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='uq__credential__action__user',
                fields=['credential', 'action', 'user']
            ),
            models.UniqueConstraint(
                name='uq__credential__action__group',
                fields=['credential', 'action', 'group']
            ),
            models.UniqueConstraint(
                name='uq__credential__action__team',
                fields=['credential', 'action', 'team']
            )
        ]

    class Action(models.TextChoices):
        VIEW = 'VIEW', _("View")
        CHANGE = 'CHANGE', _("Change")

    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="grants",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="grants",
        null=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="grants",
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="grants",
        null=True
    )
    action = models.CharField(
        verbose_name=_("action"),
        max_length=150,
        choices=Action.choices,
        default=Action.VIEW
    )


class CredetialShare(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="uq__shared_by__shared_with_user",
                fields=['shared_by', 'shared_with_user']
            ),
            models.UniqueConstraint(
                name="uq__shared_by__shared_with_group",
                fields=['shared_by', 'shared_with_group']
            ),
            models.UniqueConstraint(
                name="uq__shared_by__shared_with_team",
                fields=['shared_by', 'shared_with_team']
            )
        ]

    shared_by = models.ForeignKey(
        User,
        db_column="shared_by",
        related_name="shares_by_me",
        on_delete=models.CASCADE,
        verbose_name=_("shared by")
    )
    shared_with_user = models.ForeignKey(
        User,
        db_column="shared_with_user",
        related_name="shares_with_me",
        on_delete=models.CASCADE,
        verbose_name=_("shared with user")
    )
    shared_with_group = models.ForeignKey(
        Group,
        db_column="shared_with_group",
        related_name="shares",
        on_delete=models.CASCADE,
        verbose_name=_("shared with group")
    )
    shared_with_team = models.ForeignKey(
        Team,
        db_column="shared_with_team",
        related_name="shares",
        on_delete=models.CASCADE,
        verbose_name=_("shared with team")
    )
    until = models.DateTimeField(
        verbose_name=_("shared until")
    )
