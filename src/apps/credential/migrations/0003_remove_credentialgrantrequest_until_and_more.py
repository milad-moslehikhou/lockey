# Generated by Django 4.2.19 on 2025-02-14 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credential', '0002_credentialgrantrequest_credentialgrant_until_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialgrantrequest',
            name='until',
        ),
        migrations.AlterField(
            model_name='credentialgrant',
            name='until',
            field=models.DateTimeField(null=True, verbose_name='granted until'),
        ),
    ]
