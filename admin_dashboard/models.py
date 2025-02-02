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


