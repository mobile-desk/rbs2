from django.db import models
from django.contrib.auth.models import User

class CardApplication(models.Model):
    CARD_CHOICES = [
        ('PBT', 'Purchase & Balance Transfer'),
        ('LBT', 'Longer Balance Transfer'),
        ('BT', 'Balance Transfer'),
        ('RBC', 'The Royal Bank Credit Card'),
        ('RWD', 'Reward credit card'),
        ('RBK', 'Reward Black credit card'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=3, choices=CARD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_card_type_display()} - {self.status}"
    
    class Meta:
        ordering = ['-application_date']