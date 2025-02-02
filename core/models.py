
from django.db import models

class SiteSettings(models.Model):
    btc_active = models.BooleanField(default=True)





from django.contrib.auth.models import User

class NSiteSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    btc_active = models.BooleanField(default=True)