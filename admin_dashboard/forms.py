from django import forms
from accounts.models import Passport, Account
from transactions.models import InternationalTransfer
from django.contrib.auth.models import User



class PassportForm(forms.ModelForm):

    class Meta:
        model = Passport
        fields = ['user', 'passport_image']




class AdminInternationalTransferForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = InternationalTransfer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.none()

        if 'user' in self.data:
            try:
                user_id = int(self.data.get('user'))
                self.fields['from_account'].queryset = Account.objects.filter(user_id=user_id)
            except (ValueError, TypeError):
                pass

