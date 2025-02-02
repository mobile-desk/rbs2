from django import forms

class BTCTopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=18, decimal_places=8)