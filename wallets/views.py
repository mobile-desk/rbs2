from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, BTCWallet
import random

def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

@login_required
def create_account(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        account_number = generate_account_number()
        
        account = Account.objects.create(
            user=request.user,
            account_number=account_number,
            account_type=account_type,
            balance=0.00
        )
        messages.success(request, 'Account created successfully!')
        return redirect('wallet:account_detail', pk=account.pk)
    
    return render(request, 'wallet/create_account.html')

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    btc_wallet = BTCWallet.objects.get(user=request.user)
    context = {
        'accounts': accounts,
        'btc_wallet': btc_wallet
    }
    return render(request, 'wallet/account_list.html', context)

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    return render(request, 'wallet/account_detail.html', {'account': account})