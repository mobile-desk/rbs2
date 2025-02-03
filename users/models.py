from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=10, blank=True, null=True)
    business_postcode = models.CharField(max_length=10, blank=True, null=True)
    customer_number = models.CharField(max_length=10, unique=True)
    pin = models.CharField(max_length=4)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return f"{self.user.username}'s Profile"




class Mailbox(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.date.strftime('%Y-%m-%d %H:%M')}"

