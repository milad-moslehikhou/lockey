from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class GroupType(models.Model):
    groups = models.ManyToManyField(
        Group,
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=150
    )
