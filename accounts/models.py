from django.db import models
from django.contrib.auth.models import User




class Account(models.Model):

    STATUS_CHOICES = [
        ('on_hold', 'On Hold'),
        ('dormant', 'Dormant'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')



    def __str__(self):
        return f"{str(self.balance)} - {self.account_type} - {self.account_number}"


class Passport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    passport_image = models.ImageField(upload_to='passports/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Passport"





class BTCWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    def __str__(self):
        return f"{self.user.username}'s BTC Wallet"

