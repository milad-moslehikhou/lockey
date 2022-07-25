from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    class Meta:
        ordering = ['-id']

    name = models.CharField(
        verbose_name=_('name'),
        max_length=150
    )
    groups = models.ManyToManyField(
        Group,
    )

    def __str__(self):
        return self.name
