from django import forms
from wallets.models import Account
from django.utils import timezone
from .models import InternationalTransfer



class PaymentForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=None, label="From Account")
    to_account = forms.CharField(max_length=100, label="To Account")
    bank_name = forms.CharField(max_length=100, label="Bank Name")
    account_name = forms.CharField(max_length=100, label="Account Name")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=100)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)




class InternationalTransferForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
    ]

    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    reason_for_payment = forms.CharField(max_length=200, required=True)
    payment_reference = forms.CharField(max_length=100, required=False)

    class Meta:
        model = InternationalTransfer
        exclude = ['user', 'date', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['from_account'].queryset = user.account_set.all()




