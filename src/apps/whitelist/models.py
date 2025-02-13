from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class Whitelist(models.Model):
    ip = models.GenericIPAddressField(
        verbose_name=_("ip address"),
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="whitelist", null=True)

    def __str__(self):
        return f"{self.user}@{self.ip}"
