from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.team.models import Team
from apps.user.models import User


class Folder(models.Model):
    class Meta:
        permissions = (
            ("add_public_folder", "Can add public folder"),
        )

    name = models.CharField(
        verbose_name=_("name"),
        max_length=150
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
        on_delete=models.RESTRICT,
        related_name="child",
        null=True
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
