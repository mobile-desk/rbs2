import json
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User




class VerificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tax_code_required = models.BooleanField(default=True)
    imf_code_required = models.BooleanField(default=True)
    otp_required = models.BooleanField(default=True)
    anti_terrorist_code_required = models.BooleanField(default=True)
    anti_money_laundering_code_required = models.BooleanField(default=True)
    
    @staticmethod
    def get_codes():
        with open(settings.BASE_DIR / 'verification_codes.json', 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_codes(codes):
        with open(settings.BASE_DIR / 'verification_codes.json', 'w') as f:
            json.dump(codes, f, indent=2)






class AdminAccountDetails(models.Model):
    ACCOUNT_TYPES = [
        ('btc', 'Bitcoin'),
        ('eth', 'Ethereum'),
        ('bank', 'Bank Account'),
        ('usdt', 'USDT')
    ]
    
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, unique=True)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    additional_info = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_account_type_display()} Account"


