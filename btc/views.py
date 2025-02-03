from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BTCTopUpForm
from .models import BTCTransaction
from users.models import CustomerProfile

@login_required
def btc_topup(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    if request.method == 'POST':
        form = BTCTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction = BTCTransaction.objects.create(user=request.user, amount=amount)
            return redirect('btc_payment', transaction_id=transaction.id)
    else:
        form = BTCTopUpForm()
    return render(request, 'btc/topup.html', {'form': form})

@login_required
def btc_payment(request, transaction_id):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    transaction = BTCTransaction.objects.get(id=transaction_id)
    btc_address = "your_btc_address_here"  # Replace with actual BTC address
    return render(request, 'btc/payment.html', {'transaction': transaction, 'btc_address': btc_address})


@login_required
def user_btc_transactions(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    transactions = BTCTransaction.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'transactions': transactions
    }
    return render(request, 'btc/user_transactions.html', context)

