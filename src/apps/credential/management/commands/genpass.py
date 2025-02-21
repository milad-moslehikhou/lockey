import random
import secrets
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.credential.models import Credential, CredentialSecret
from apps.user.models import User


class Command(BaseCommand):
    help = "Generate new secret for credentials"

    def handle(self, *args, **options):
        try:
            user = User.objects.filter(username="admin").first()
            if user is None:
                self.stderr.write(self.style.ERROR("We need a user with username='admin' to perform command!"))
                return
            credentials = Credential.objects.filter(auto_genpass=True)
            if len(credentials) == 0:
                self.stdout.write("No credential found!")
                return
            self.stdout.write(f"There are {len(credentials)} credential that marked for auto generate password,")
            user_input = input("Are you sure to continue [yes|no]? ")
            if user_input != "yes":
                return
            category = uuid.uuid4()
            for credential in credentials:
                char_choices = list(settings.PASSWORD_ALLOWED_CHARS)
                random.shuffle(char_choices)
                password = "".join(secrets.choice(char_choices) for i in range(settings.PASSWORD_LENGHT))
                secret = CredentialSecret(
                    password=password,
                    expire_at=datetime.now() + timedelta(days=90),
                    category=category,
                    credential=credential,
                    created_by=user,
                )
                secret.save()
            self.stdout.write(self.style.SUCCESS(f"All new secrets categorized under {category}"))
        except Exception as e:
            raise CommandError(e) from None
