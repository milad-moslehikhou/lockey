from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.messaging import send_message

from .models import CredentialGrantRequest


@receiver(post_save, sender=CredentialGrantRequest)
def grant_request_created(sender, instance: CredentialGrantRequest, created, *kwargs):
    mobile = instance.respondent.mobile
    content = instance.request_string
    if created and mobile:
        send_message(to=mobile, content=content)
