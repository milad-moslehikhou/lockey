
from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from django_cryptography.fields import encrypt
from apps.folder.models import Folder

from apps.team.models import Team
from apps.user.models import User


class Credential(models.Model):
    class Meta:
        permissions = (
            ("add_public_credential", "Can add public credential"),
        )

    class Importancy(models.TextChoices):
        HIGH = 'HIGH', _("High")
        MEDUIM = 'MEDUIM', _("Meduim")
        LOW = 'LOW', _("Low")

    name = models.CharField(
        verbose_name=_("name"),
        max_length=150
    )
    username = models.CharField(
        verbose_name=_("username"),
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
        verbose_name=_("public"),
        default=False
    )
    auto_genpass = models.BooleanField(
        verbose_name=_("auto generate"),
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
        max_length=255,
        null=True
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.DO_NOTHING,
        verbose_name=_("folder"),
        related_name="credentials",
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
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.username}@{self.name}'


class CredentialSecret(models.Model):
    password = encrypt(
        models.CharField(
            verbose_name=_("password"),
            max_length=150
        )
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


class CredentialFavorite(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='uq__credential__user',
                fields=['credential', 'user']
            ),
        ]

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


class CredentialShare(models.Model):
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

    credential = models.ForeignKey(
        Credential,
        on_delete=models.CASCADE,
        related_name="share_with",
    )
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
