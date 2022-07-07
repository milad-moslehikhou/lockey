from django.db import models

from .user import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        default='default.jpg',
        upload_to='avatars/'
    )
