from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.team.models import Team
from apps.user.models import User
from apps.credential.models import Credential


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
