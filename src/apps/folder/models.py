from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.credential.models import Credential
from apps.team.models import Team
from apps.user.models import User


class Folder(models.Model):
    class Meta:
        permissions = (
            ("add_public_folder", "Can add public folder"),
        )

    class Icon(models.TextChoices):
        DEFAULT = 'default.ico', _("Default")
        SERVER = 'server.ico', _("Server")
        LINUX_SERVER = 'linux_server.ico', _("Linux Server")
        WINDOWS_SERVER = 'windows_server.ico', _("Windows Server")
        DATABASE = 'database.ico', _("Database")
        FIREWALL = 'firewall.ico', _("Firewall")

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
        verbose_name=_("color"),
        max_length=7,
        default='#ffffff'
    )
    is_public = models.BooleanField(
        verbose_name=_("public"),
        default=False
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child",
        null=True
    )
    credentials = models.ManyToManyField(
        Credential,
        verbose_name=_("credentials"),
        related_name="folders",
        blank=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="folders"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="folders"
    )
