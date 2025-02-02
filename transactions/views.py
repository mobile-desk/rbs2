from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, PendingTransaction, Receipt, Beneficiary, ScheduledPayment, InternationalTransfer
from accounts.models import Account
from django.utils import timezone
from .forms import PaymentForm, InternationalTransferForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from admin_dashboard.models import VerificationSettings

VALID_TAX_CODES = ['TX1257L12', 'TX12356', 'A1B2C3', 'X9Y8Z7', 'M5N6P7', 'Q2W3E4', 'R5T6Y7', 
               'U8I9O0', 'F4G5H6', 'J7K8L9', 'S1D2F3', 'Z9X8C7',
               'V6B7N8', 'A3S4D5', 'G8H9J0', 'K2L3M4', 'W5E6R7',
               'T9Y0U1', 'I3O4P5', 'Q7W8E9', 'R1T2Y3', 'U4I5O6']

VALID_OTP_CODES = ['TX1257L12', 'TX12356', 'A1B2C3', 'X9Y8Z7', 'M5N6P7', 'Q2W3E4', 'R5T6Y7', 
               'U8I9O0', 'F4G5H6', 'J7K8L9', 'S1D2F3', 'Z9X8C7',
               'V6B7N8', 'A3S4D5', 'G8H9J0', 'K2L3M4', 'W5E6R7',
               'T9Y0U1', 'I3O4P5', 'Q7W8E9', 'R1T2Y3', 'U4I5O6']

IMF_CODES = ['IMF81672956']



def check_tax_code(code):
    codes = VerificationSettings.get_codes()
    return code.strip() in [c.strip() for c in codes['VALID_TAX_CODES']]

def check_imf_code(code):
    codes = VerificationSettings.get_codes()
    return code.strip() in [c.strip() for c in codes['IMF_CODES']]

def check_otp(code):
    codes = VerificationSettings.get_codes()
    return code.strip() in [c.strip() for c in codes['VALID_OTP_CODES']]


def check_anti_terrorist_code(code):
    codes = VerificationSettings.get_codes()
    return code.strip() in [c.strip() for c in codes['ANTI_TERRORIST_CODES']]

def check_anti_money_laundering_code(code):
    codes = VerificationSettings.get_codes()
    return code.strip() in [c.strip() for c in codes['ANTI_MONEY_LAUNDERING_CODES']]


@login_required
def pat(request):
    return render(request, 'transactions/pat.html')

@login_required
def transaction_list(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-timestamp')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})



from django.utils import timezone

from admin_dashboard.models import VerificationSettings

def get_verification_settings():
    return VerificationSettings.objects.first() or VerificationSettings.objects.create()


@login_required
def submit_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            amount = form.cleaned_data['amount']

            if from_account.status != 'active':
                messages.error(request, 'The selected account is not active. Please choose an active account.')
                return render(request, 'transactions/submit_payment.html', {'form': form})

            if from_account.balance >= amount:
                receipt = Receipt.objects.create(
                    sender=request.user,
                    amount=amount,
                    recipient_account=form.cleaned_data['to_account'],
                    description=form.cleaned_data['description'],
                    date_time=timezone.now()  # Set the timestamp to the current time
                )

                request.session['payment_data'] = {
                    'from_account_id': from_account.id,
                    'amount': str(amount),
                    'bank_name': form.cleaned_data['bank_name'],
                    'account_name': form.cleaned_data['account_name'],
                    'description': form.cleaned_data['description'],
                    'receipt_id': str(receipt.id)
                }
                return redirect('transactions:verify_tax_code')
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = PaymentForm(request.user)
    return render(request, 'transactions/submit_payment.html', {'form': form})


@login_required
def verify_tax_code(request):
    settings = get_verification_settings()
    if not settings.tax_code_required:
        return redirect('transactions:verify_anti_terrorist_code')
    
    if request.method == 'POST':
        code = request.POST.get('tax_code')
        if check_tax_code(code):
            return redirect('transactions:verify_anti_terrorist_code')
        else:
            messages.error(request, 'Invalid Code.')
    return render(request, 'transactions/verify_tax_code.html')


@login_required
def verify_anti_terrorist_code(request):
    settings = get_verification_settings()
    if not settings.anti_terrorist_code_required:
        return redirect('transactions:verify_anti_money_laundering_code')
    
    if request.method == 'POST':
        code = request.POST.get('anti_terrorist_code')
        if check_anti_terrorist_code(code):
            return redirect('transactions:verify_anti_money_laundering_code')
        else:
            messages.error(request, 'Invalid Code.')
    return render(request, 'transactions/verify_anti_terrorist_code.html')

@login_required
def verify_anti_money_laundering_code(request):
    settings = get_verification_settings()
    if not settings.anti_money_laundering_code_required:
        return redirect('transactions:verify_imf_code')
    
    if request.method == 'POST':
        code = request.POST.get('anti_money_laundering_code')
        if check_anti_money_laundering_code(code):
            return redirect('transactions:verify_imf_code')
        else:
            messages.error(request, 'Invalid Code.')
    return render(request, 'transactions/verify_anti_money_laundering_code.html')


@login_required
def verify_imf_code(request):
    settings = get_verification_settings()
    if not settings.imf_code_required:
        return redirect('transactions:verify_otp')
    
    if request.method == 'POST':
        code = request.POST.get('imf_code')
        if check_imf_code(code):
            return redirect('transactions:verify_otp')
        else:
            messages.error(request, 'Invalid Code.')
    return render(request, 'transactions/verify_imf_code.html')


@login_required
def verify_otp(request):
    settings = get_verification_settings()
    if not settings.otp_required:
        return redirect('transactions:process_transaction')
    
    if request.method == 'POST':
        code = request.POST.get('otp')
        if check_otp(code):
            return redirect('transactions:process_transaction')
        else:
            messages.error(request, 'Invalid Code.')
    return render(request, 'transactions/verify_otp.html')




from django.utils import timezone


@login_required
def process_transaction(request):
    payment_data = request.session.get('payment_data')
    if payment_data:
        from_account = Account.objects.get(id=payment_data['from_account_id'])
        Transaction.objects.create(
            account=from_account,
            bank_name=payment_data['bank_name'],
            account_name=payment_data['account_name'],
            amount=-Decimal(payment_data['amount']),
            transaction_type='Debit',
            description=payment_data['description'],
            timestamp=timezone.now()  # Add this line to set the timestamp
        )
        from_account.balance -= Decimal(payment_data['amount'])
        from_account.save()
        del request.session['payment_data']
        return redirect('transactions:transaction_success')
    return redirect('transactions:submit_payment')




@login_required
def transaction_success(request):
    return render(request, 'transactions/transaction_success.html')

def display_receipt(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    return render(request, 'transactions/receipt.html', {'receipt': receipt})



@login_required
def create_international_transfer(request):
    if request.method == 'POST':
        form = InternationalTransferForm(request.POST, user=request.user)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            
            if transfer.from_account.status != 'active':
                messages.error(request, 'The selected account is not active. Please choose an active account.')
                return render(request, 'transactions/create_international_transfer.html', {'form': form})
            

            # Create a transaction object
            Transaction.objects.create(
                account=transfer.from_account,
                amount=-transfer.amount,
                transaction_type='International Transfer',
                description=f"International transfer to {transfer.recipient_name}",
                timestamp=timezone.now()  # Add this line to set the timestamp
            )

            transfer = InternationalTransfer.objects.create(
                user=request.user,
                from_account=form.cleaned_data['from_account'],
                recipient_name=form.cleaned_data['recipient_name'],
                recipient_account=form.cleaned_data['recipient_account'],
                recipient_bank=form.cleaned_data['recipient_bank'],
                
                amount=form.cleaned_data['amount'],
                currency=form.cleaned_data['currency'],
                status='Pending'
            )

            
            return redirect('transactions:transfer_success')
    else:
        form = InternationalTransferForm(user=request.user)
    return render(request, 'transactions/create_international_transfer.html', {'form': form})


def transfer_success(request):
    return render(request, 'transactions/transfer_success.html')



