from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BTCWallet
import hashlib
import random

@receiver(post_save, sender=User)
def create_btc_wallet(sender, instance, created, **kwargs):
    if created:
        BTCWallet.objects.create(user=instance, wallet_address=generate_btc_address())

def generate_btc_address():
    # Generate a random BTC-like address
    random_bytes = random.randbytes(32)
    address = hashlib.sha256(random_bytes).hexdigest()[:34]
    return f"1{address}"