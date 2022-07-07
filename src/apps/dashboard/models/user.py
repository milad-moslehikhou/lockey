from django.db import models
from django.contrib.auth.models import User

from .tenant import Tenant


User.add_to_class(
    'tenant',
    models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        null=True
    )
)
