from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet , Currency

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            default = Currency.objects.get(code='INR')
        except Currency.DoesNotExist:
            return
        Wallet.objects.create(user=instance, currency=default)
