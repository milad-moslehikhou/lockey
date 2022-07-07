from django.db import models
from django.contrib.auth.models import Group

from .tenant import Tenant


Group.add_to_class(
    'tenant',
    models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        null=True
    )
)
