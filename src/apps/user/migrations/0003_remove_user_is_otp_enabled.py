# Generated by Django 4.2.19 on 2025-02-14 09:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_user_is_otp_enabled_user_otp_secret"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_otp_enabled",
        ),
    ]
