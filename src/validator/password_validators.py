import re
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _
from django.utils import timezone

from apps.user.models import PasswordRecord


class ComplexityValidator:

    def __init__(self, **kwargs):
        self.min_char_categories = kwargs.pop('min_char_categories', 4)
        self.min_chars_of_each_type = [
            ('min_numeric', r'[0-9]', 'number'),
            ('min_uppercase', r'[A-Z]', 'uppercase letter'),
            ('min_lowercase', r'[a-z]', 'lowercase letters'),
            ('min_special_chars', r'[^0-9A-Za-z]', 'special charcters'),
        ]
        for attr, _regex, _name in self.min_chars_of_each_type:
            setattr(self, attr, kwargs.get(attr, 1))

    def validate(self, password, user=None):
        password_valid = True
        errors = []
        char_types_contained = 0
        for attr, regex, name in self.min_chars_of_each_type:
            find = re.findall(regex, password)
            required = getattr(self, attr)
            if len(find) < required:
                password_valid = False
                errors.append(f"{required} {name}")
            if find:
                char_types_contained += 1

        if char_types_contained < self.min_char_categories:
            password_valid = False

        if not password_valid:
            raise ValidationError(
                f"This password is too simple. It must contain at least {', '.join(errors)}.",
                code='password_complexity',
            )

    def get_help_text(self):
        requirements = []
        for attr, regex, name in self.min_chars_of_each_type:
            required = getattr(self, attr)
            if required:
                requirements.append(f"{required} {name} characters")

        return f"This password is too simple. It must contain at least {', '.join(requirements)}."


class ReusedValidator:

    def __init__(self, record_length=3):
        if record_length <= 0:
            raise ValueError('record_length must be larger than 0.')
        self.record_length = record_length

    def validate(self, password, user=None):
        if user is None:
            return None

        stored_password_records = (
            PasswordRecord.objects.filter(user=user)
        )
        if not stored_password_records:
            return None
        for record in stored_password_records[:self.record_length]:
            if check_password(password, record.password):
                raise ValidationError(
                    self.get_help_text(),
                    code='password_repeated',
                )

    def get_help_text(self):
        return _(
            f"The password cannot be the same as it used the last {
                self.record_length} times."
        )


class MinimumChangeIntervalValidator:

    def __init__(self, min_interval_days=1):
        self.min_interval = timedelta(days=min_interval_days)
        self.requires_context = True

    def validate(self, password, user=None):
        if user is None or user.force_change_pass:
            return None
        try:
            latest_password_record = (
                PasswordRecord.objects.filter(user=user).latest()
            )
        except PasswordRecord.DoesNotExist:
            return None
        if (timezone.now() - latest_password_record.date) < self.min_interval:
            raise ValidationError(
                self.get_help_text(),
                code='password_reset_interval',
            )

    def get_help_text(self):
        return _(
            f"The password must be at least {
                self.min_interval.days} days since the last change."
        )
