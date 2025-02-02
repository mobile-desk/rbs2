from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer_number = models.CharField(max_length=11, unique=True, editable=False)
    passport = models.CharField(max_length=50, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('banned', 'Banned'),
        ('deactivated', 'Deactivated'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.customer_number:
            self.customer_number = ''.join(random.choices(string.digits, k=11))
        super().save(*args, **kwargs)
