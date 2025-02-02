from django.db import models
from wallets.models import Account
from django.contrib.auth.models import User
import uuid




class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"




class InternationalTransfer(models.Model):
    # Sender's Details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField(blank=True, null=True)

    # Receiver's Details
    recipient_name = models.CharField(max_length=100)
    recipient_address = models.TextField()
    recipient_phone = models.CharField(max_length=20)
    recipient_email = models.EmailField(blank=True, null=True)

    # Bank Details
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='international_transfers_sent')
    recipient_bank = models.CharField(max_length=100)
    recipient_bank_address = models.TextField()
    swift_bic = models.CharField(max_length=11)
    iban = models.CharField(max_length=34, blank=True, null=True)
    recipient_account = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=9, blank=True, null=True)

    # Transfer Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    reason_for_payment = models.CharField(max_length=200)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} to {self.recipient_name}"





class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    custom_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.custom_name} by {str(self.user)}"

class ScheduledPayment(models.Model):
    from_account = models.CharField(max_length=20)
    to_account = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.amount)} to {str(self.to_account)} on {str(self.payment_date)}"

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_receipts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_account = models.CharField(max_length=20)
    recipient_bank_name = models.CharField(max_length=100)
    recipient_account_name = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Receipt {self.id}: {self.sender.get_full_name()} to {self.recipient_account}"

    @property
    def sender_name(self):
        return f"{self.sender.first_name} {self.sender.last_name}"

    @property
    def recipient_details(self):
        return f"{self.recipient_account_name} - {self.recipient_account}"

class PendingTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.CharField(max_length=20)
    to_account = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_now = models.BooleanField()
    payment_date = models.DateTimeField(null=True, blank=True)
    save_beneficiary = models.BooleanField()
    beneficiary_name = models.CharField(max_length=255, blank=True)
    receipt_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending Transaction for {self.user.username}"