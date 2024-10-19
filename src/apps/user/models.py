from typing import Any
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        """
        Create and save a user with the given fields.
        """
        if not username:
            raise ValueError("The given username must be set")
        username = User.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        record = PasswordRecord(user=user, password=user.password)
        record.save()
        return user

    def create_superuser(self, username, password=None):
        """
        Create and save a user with the given username, email, and password.
        """
        username = User.normalize_username(username)
        user = self.create(username=username, password=password)
        user.is_superuser = True
        user.force_change_pass = False
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[validate_password])
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    force_change_pass = models.BooleanField(
        verbose_name=_("force change password"),
        default=True,
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        auto_now_add=True
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=150,
        null=True
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=150,
        null=True
    )
    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to='avatars/',
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        """
            Return the first_name plus the last_name, with a space in between.
            """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def short_name(self):
        """Return the short name for the user."""
        return self.first_name


class PasswordRecordManager(models.Manager):

    def create(self, **kwargs: Any) -> Any:
        self.objects.all()[:-3].delete()
        return super().create(**kwargs)


class PasswordRecord(models.Model):
    user = models.ForeignKey(
        User,
        related_name='password_records',
        on_delete=models.CASCADE,
        editable=False
    )

    password = models.CharField(
        verbose_name=_('password hash'),
        max_length=128,
        editable=False
    )
    date = models.DateTimeField(
        verbose_name=_('date'),
        auto_now_add=True,
        editable=False
    )

    objects = PasswordRecordManager()

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
