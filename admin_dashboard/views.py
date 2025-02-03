from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from transactions.models import Transaction, InternationalTransfer
from users.models import CustomerProfile, Mailbox
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import CustomerProfile
from accounts.models import Account, Passport, BTCWallet
import random
from django.utils import timezone
from datetime import datetime

from django import forms
from django.http import FileResponse
from .forms import PassportForm, AdminInternationalTransferForm
from core.models import NSiteSettings
from django.db import IntegrityError

from django.contrib.auth.forms import SetPasswordForm



def is_admin(user):
    return user.is_staff




def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard:user_list')
        else:
            messages.error(request, 'Invalid email or password, or insufficient permissions.')
    return render(request, 'admin_dashboard/admin_login.html')






def user_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')
    users = User.objects.all()
    return render(request, 'admin_dashboard/user_list.html', {'users': users})






def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f'{user.username} is now an admin.')
    return redirect('admin_dashboard:user_list')

def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = False
    user.save()
    messages.success(request, f'{user.username} is no longer an admin.')
    return redirect('admin_dashboard:user_list')




'''
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    customer_profile = CustomerProfile.objects.get(user=user)
    
    try:
        passport = Passport.objects.get(user=user)
    except Passport.DoesNotExist:
        passport = None
    
    accounts = Account.objects.filter(user=user)

    if request.method == 'POST':
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        customer_profile.middle_name = request.POST['middle_name']
        customer_profile.date_of_birth = request.POST['date_of_birth']
        customer_profile.postcode = request.POST['postcode']
        customer_profile.save()

        if passport:
            passport.passport_number = request.POST['passport_number']
            passport.issue_date = request.POST['issue_date']
            passport.expiry_date = request.POST['expiry_date']
            passport.country_of_issue = request.POST['country_of_issue']
            passport.save()
        elif 'passport_number' in request.POST:
            # Create a new passport if the user doesn't have one
            Passport.objects.create(
                user=user,
                passport_number=request.POST['passport_number'],
                issue_date=request.POST['issue_date'],
                expiry_date=request.POST['expiry_date'],
                country_of_issue=request.POST['country_of_issue']
            )

        for account in accounts:
            account.status = request.POST['account_status']
            account.save()

        messages.success(request, f'{user.username} has been updated.')
        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/edit_user.html', {
        'user': user,
        'customer_profile': customer_profile,
        'passport': passport,
        'accounts': accounts,
        'status_choices': Account.STATUS_CHOICES
    })

'''





def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    customer_profile = CustomerProfile.objects.get(user=user)
    
    try:
        passport = Passport.objects.get(user=user)
    except Passport.DoesNotExist:
        passport = None
    
    accounts = Account.objects.filter(user=user)

    if request.method == 'POST':
        try:
            new_username = request.POST['username']
            if new_username != user.username:
                User.objects.get(username=new_username)
                messages.error(request, 'This username is already taken.')
            else:
                user.username = new_username
                user.save()

                # Update the customer number to match the new username
                customer_profile.customer_number = new_username
                customer_profile.save()


                user.email = request.POST['email']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                
                if 'date_joined' in request.POST:
                    user.date_joined = timezone.make_aware(datetime.strptime(request.POST['date_joined'], '%Y-%m-%d'))
                
                user.save()

                customer_profile.middle_name = request.POST['middle_name']
                customer_profile.date_of_birth = request.POST['date_of_birth']
                customer_profile.postcode = request.POST['postcode']
                customer_profile.save()





                if passport:
                    passport.passport_number = request.POST['passport_number']
                    passport.issue_date = request.POST['issue_date']
                    passport.expiry_date = request.POST['expiry_date']
                    passport.country_of_issue = request.POST['country_of_issue']
                    passport.save()
                elif 'passport_number' in request.POST:
                    Passport.objects.create(
                        user=user,
                        passport_number=request.POST['passport_number'],
                        issue_date=request.POST['issue_date'],
                        expiry_date=request.POST['expiry_date'],
                        country_of_issue=request.POST['country_of_issue']
                    )

                for account in accounts:
                    account.status = request.POST['account_status']
                    account.save()

                messages.success(request, f'{user.username} has been updated.')
                return redirect('admin_dashboard:user_list')
            
        except User.DoesNotExist:
            user.username = new_username
            user.save()
            messages.success(request, f'Username updated to {new_username}')
        except IntegrityError:
            messages.error(request, 'This username is already taken.')


    return render(request, 'admin_dashboard/edit_user.html', {
        'user': user,
        'customer_profile': customer_profile,
        'passport': passport,
        'accounts': accounts,
        'status_choices': Account.STATUS_CHOICES
    })










def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User has been deleted.')
        return redirect('admin_dashboard:user_list')
    return render(request, 'admin_dashboard/delete_user.html', {'user': user})









def user_detail(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    user = get_object_or_404(User, id=user_id)
    accounts = Account.objects.filter(user=user)
    customer_profile = CustomerProfile.objects.get(user=user)

    try:
        passport = Passport.objects.get(user=user)
    except Passport.DoesNotExist:
        passport = None

    context = {
        'user': user,
        'accounts': accounts,
        'customer_profile': customer_profile,
        'passport': passport
    }

    return render(request, 'admin_dashboard/user_detail.html', context)


def create_user(request):
    CUSTOMER_TYPES = [
        ('personal', 'PERSONAL ACCOUNT'),
        ('business', 'BUSINESS ACCOUNT'),
        
        ('checking_account', 'CHECKING ACCOUNT'),
        ('premium_offshore_account', 'PREMIUM OFFSHORE ACCOUNT'),
        ('numbered_account', 'NUMBERED ACCOUNT'),
    ]
    if request.method == 'POST':
        # Generate username
        username = ''.join([str(random.randint(0, 9)) for _ in range(10)])

        # Create user
        user = User.objects.create_user(
            username=username,
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name']
        )

        # Create customer profile
        CustomerProfile.objects.create(
            user=user,
            customer_type=request.POST['customer_type'],
            middle_name=request.POST.get('middle_name'),
            date_of_birth=request.POST['date_of_birth'],
            postcode=request.POST.get('postcode'),
            business_postcode=request.POST.get('business_postcode'),
            customer_number=username,
            pin=request.POST['pin']
        )

        # Create savings and current accounts
        Account.objects.create(
            user=user,
            account_number=''.join([str(random.randint(0, 9)) for _ in range(10)]),
            account_type='Savings',
            balance=0.00
        )
        Account.objects.create(
            user=user,
            account_number=''.join([str(random.randint(0, 9)) for _ in range(10)]),
            account_type='Current',
            balance=0.00
        )

        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/create_user.html', {'customer_types': CUSTOMER_TYPES})





class ManualTransactionForm(forms.ModelForm):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment', 'Payment'),
        ('fee', 'Fee'),
        ('interest', 'Interest'),
        ('international_transfer', 'International Transfer'),
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]


    
    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES)

    timestamp = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )


    class Meta:
        model = Transaction
        fields = ['account', 'bank_name', 'account_name', 'amount', 'transaction_type', 'description', 'timestamp']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.timestamp = self.cleaned_data['timestamp']
        if commit:
            instance.save()
        return instance
    



def create_transaction(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')
    if request.method == 'POST':
        form = ManualTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:transaction_list')
    else:
        form = ManualTransactionForm()

    # Add classes to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-input'

    return render(request, 'admin_dashboard/create_transaction.html', {'form': form})




def transaction_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')
    transactions = Transaction.objects.all()
    return render(request, 'admin_dashboard/transaction_list.html', {'transactions': transactions})




from django.shortcuts import get_object_or_404, redirect
from transactions.models import Transaction


class EditManualTransactionForm(forms.ModelForm):

   
    timestamp = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']
    )



    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description', 'timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['account'] = forms.CharField(disabled=True, initial=self.instance.account)
            self.fields['timestamp'].initial = self.instance.timestamp.strftime('%Y-%m-%dT%H:%M')




def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = EditManualTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.timestamp = form.cleaned_data['timestamp']
            transaction.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect('admin_dashboard:transaction_list')

    else:
        form = EditManualTransactionForm(instance=transaction)
    return render(request, 'admin_dashboard/edit_transaction.html', {'form': form, 'transaction': transaction})







def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('admin_dashboard:transaction_list')
    return render(request, 'admin_dashboard/delete_transaction.html', {'transaction': transaction})






def send_mail_to_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    if request.method == 'POST':
        recipient = User.objects.get(id=request.POST['recipient'])
        mailbox = Mailbox.objects.create(
            recipient=recipient,
            sender=request.user,
            subject=request.POST['subject'],
            content=request.POST['content'],
            priority=request.POST['priority']
        )
        send_mail(
            subject=request.POST['subject'],
            message=request.POST['content'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
        )
        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/send_mail.html')




def send_direct_email(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    if request.method == 'POST':
        send_mail(
            subject=request.POST['subject'],
            message=request.POST['content'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.POST['email']],
        )
        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/send_direct_email.html')








def manage_passports(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    passports = Passport.objects.all()
    return render(request, 'admin_dashboard/manage_passports.html', {'passports': passports})




def add_edit_passport(request, user_id=None):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    passport = None
    if user_id:
        passport = get_object_or_404(Passport, user_id=user_id)

    if request.method == 'POST':
        form = PassportForm(request.POST, request.FILES, instance=passport)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:manage_passports')
    else:
        form = PassportForm(instance=passport)

    return render(request, 'admin_dashboard/add_edit_passport.html', {'form': form, 'passport': passport})





def delete_passport(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    passport = get_object_or_404(Passport, user_id=user_id)
    passport.delete()
    return redirect('admin_dashboard:manage_passports')


def download_passport(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    passport = get_object_or_404(Passport, user_id=user_id)
    if passport.passport_image:
        return FileResponse(passport.passport_image.open(), as_attachment=True, filename=f'{passport.user.username}_passport.jpg')
    return redirect('admin_dashboard:manage_passports')





def admin_create_international_transfer(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')
    if request.method == 'POST':
        form = AdminInternationalTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save()


            # Create a transaction object
            Transaction.objects.create(
                account=transfer.from_account,
                amount=-transfer.amount,
                transaction_type='International Transfer',
                description=f"International transfer to {transfer.recipient_name}",
                timestamp=transfer.date
            )

            return redirect('admin_dashboard:international_transfer_list')
    else:
        form = AdminInternationalTransferForm()
    return render(request, 'admin_dashboard/create_international_transfer.html', {'form': form})





def list_btc_wallets(request):
    wallets = BTCWallet.objects.all()
    return render(request, 'admin_dashboard/list_btc_wallets.html', {'wallets': wallets})

def create_btc_wallet(request):
    users_without_wallet = User.objects.filter(btcwallet__isnull=True)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        wallet_address = request.POST.get('wallet_address')
        user = User.objects.get(id=user_id)
        BTCWallet.objects.create(user=user, wallet_address=wallet_address)
        return redirect('admin_dashboard:list_btc_wallets')
    return render(request, 'admin_dashboard/create_btc_wallet.html', {'users': users_without_wallet})

def edit_btc_wallet(request, wallet_id):
    wallet = BTCWallet.objects.get(id=wallet_id)
    if request.method == 'POST':
        wallet.wallet_address = request.POST.get('wallet_address')
        wallet.balance = request.POST.get('balance')
        wallet.save()
        return redirect('admin_dashboard:list_btc_wallets')
    return render(request, 'admin_dashboard/edit_btc_wallet.html', {'wallet': wallet})





def btc_status_control(request):
    if not request.user.is_authenticated:
        return redirect('admin_dashboard:admin_login')
    if not request.user.is_staff:
        logout(request)
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('admin_dashboard:admin_login')

    users = User.objects.all()
    user_settings = []

    for user in users:
        site_settings, created = NSiteSettings.objects.get_or_create(user=user)
        user_settings.append(site_settings)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        btc_active = request.POST.get('btc_active') == 'on'
        site_settings = NSiteSettings.objects.get(user_id=user_id)
        site_settings.btc_active = btc_active
        site_settings.save()
        messages.success(request, f'BTC status updated for user {site_settings.user.username}')
        return redirect('admin_dashboard:btc_status_control')

    return render(request, 'admin_dashboard/btc_status_control.html', {'user_settings': user_settings})



'''

def modify_balance(request, user_id):
    user = get_object_or_404(User, id=user_id)
    accounts = Account.objects.filter(user=user)

    if request.method == 'POST':
        for account in accounts:
            account.balance = request.POST.get(f'balance_{account.id}')
            account.status = request.POST.get(f'status_{account.id}')
            account.save()
        messages.success(request, f'Accounts for {user.email} have been updated.')
        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/modify_balance.html', {
        'user': user,
        'accounts': accounts,
        'status_choices': Account.STATUS_CHOICES
    })

'''







def modify_balance(request, user_id):
    user = get_object_or_404(User, id=user_id)
    accounts = Account.objects.filter(user=user)

    if request.method == 'POST':
        for account in accounts:
            new_account_number = request.POST.get(f'account_number_{account.id}')
            try:
                if new_account_number != account.account_number:
                    Account.objects.get(account_number=new_account_number)
                    messages.error(request, f'Account number {new_account_number} already exists.')
                else:
                    account.account_number = new_account_number
                    account.balance = request.POST.get(f'balance_{account.id}')
                    account.status = request.POST.get(f'status_{account.id}')
                    account.save()
            except Account.DoesNotExist:
                account.account_number = new_account_number
                account.balance = request.POST.get(f'balance_{account.id}')
                account.status = request.POST.get(f'status_{account.id}')
                account.save()
            except IntegrityError:
                messages.error(request, f'Account number {new_account_number} already exists.')

        if not messages.get_messages(request):
            messages.success(request, f'Accounts for {user.email} have been updated.')
        return redirect('admin_dashboard:user_list')

    return render(request, 'admin_dashboard/modify_balance.html', {
        'user': user,
        'accounts': accounts,
        'status_choices': Account.STATUS_CHOICES
    })






def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:user_list')
    else:
        form = SetPasswordForm(user)
    return render(request, 'admin_dashboard/change_user_password.html', {'form': form, 'user': user})










from django import forms
from django.contrib import admin
from .models import VerificationSettings




class CodeForm(forms.Form):
    VALID_TAX_CODES = forms.CharField(widget=forms.Textarea)
    VALID_OTP_CODES = forms.CharField(widget=forms.Textarea)
    IMF_CODES = forms.CharField(widget=forms.Textarea)
    ANTI_TERRORIST_CODES = forms.CharField(widget=forms.Textarea)
    ANTI_MONEY_LAUNDERING_CODES = forms.CharField(widget=forms.Textarea)

@user_passes_test(lambda u: u.is_staff)
def edit_verification_codes(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            codes = VerificationSettings.get_codes()
            for key in codes.keys():
                codes[key] = [code.strip() for code in form.cleaned_data[key].split('\n') if code.strip()]
            VerificationSettings.save_codes(codes)
            messages.success(request, "Verification codes updated successfully.")
            return redirect('admin_dashboard:edit_verification_codes')
    else:
        codes = VerificationSettings.get_codes()
        initial = {key: '\n'.join(value) for key, value in codes.items()}
        form = CodeForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Edit Verification Codes',
    }
    return render(request, 'admin_dashboard/edit_codes.html', context)

@user_passes_test(lambda u: u.is_staff)
def verification_status_control(request):
    users = User.objects.all()
    user_settings = []

    for user in users:
        settings, created = VerificationSettings.objects.get_or_create(user=user)
        user_settings.append(settings)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tax_code_required = request.POST.get('tax_code_required') == 'on'
        imf_code_required = request.POST.get('imf_code_required') == 'on'
        otp_required = request.POST.get('otp_required') == 'on'
        anti_terrorist_code_required = request.POST.get('anti_terrorist_code_required') == 'on'
        anti_money_laundering_code_required = request.POST.get('anti_money_laundering_code_required') == 'on'
        
        settings = VerificationSettings.objects.get(user_id=user_id)
        settings.tax_code_required = tax_code_required
        settings.imf_code_required = imf_code_required
        settings.otp_required = otp_required
        settings.anti_terrorist_code_required = anti_terrorist_code_required
        settings.anti_money_laundering_code_required = anti_money_laundering_code_required
        settings.save()
        
        messages.success(request, f'Verification status updated for user {settings.user.username}')
        return redirect('admin_dashboard:verification_status_control')

    return render(request, 'admin_dashboard/verification_status_control.html', {'user_settings': user_settings})





from django.conf import settings
import os
import json

def create_config_file(file_path, default_content):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_content, f, indent=2)


@user_passes_test(lambda u: u.is_staff)
def edit_config(request):
    email_config_path = os.path.join(settings.BASE_DIR, 'email_config.json')
    session_config_path = os.path.join(settings.BASE_DIR, 'session_config.json')

    if request.method == 'POST':
        email_config = {
            "EMAIL_BACKEND": request.POST.get('EMAIL_BACKEND'),
            "EMAIL_HOST": request.POST.get('EMAIL_HOST'),
            "EMAIL_PORT": int(request.POST.get('EMAIL_PORT')),
            "EMAIL_USE_SSL": request.POST.get('EMAIL_USE_SSL') == 'on',
            "EMAIL_HOST_USER": request.POST.get('EMAIL_HOST_USER'),
            "EMAIL_HOST_PASSWORD": request.POST.get('EMAIL_HOST_PASSWORD'),
            "DEFAULT_FROM_EMAIL": request.POST.get('DEFAULT_FROM_EMAIL')
        }
        session_config = {
            "SESSION_COOKIE_AGE": int(request.POST.get('SESSION_COOKIE_AGE')),
            "SESSION_SAVE_EVERY_REQUEST": request.POST.get('SESSION_SAVE_EVERY_REQUEST') == 'on',
            "SESSION_EXPIRE_AT_BROWSER_CLOSE": request.POST.get('SESSION_EXPIRE_AT_BROWSER_CLOSE') == 'on'
        }
        
        with open(email_config_path, 'w') as f:
            json.dump(email_config, f, indent=2)
        
        with open(session_config_path, 'w') as f:
            json.dump(session_config, f, indent=2)
        
        messages.success(request, "Configuration updated successfully.")
        return redirect('admin_dashboard:edit_config')
    
    with open(email_config_path, 'r') as f:
        email_config = json.load(f)
    
    with open(session_config_path, 'r') as f:
        session_config = json.load(f)
    
    context = {
        'email_config': email_config,
        'session_config': session_config,
    }
    return render(request, 'admin_dashboard/edit_config.html', context)





from django.shortcuts import render, redirect
from .models import AdminAccountDetails
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def edit_payment_details(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        account_number = request.POST.get('account_number')
        account_name = request.POST.get('account_name')
        additional_info = request.POST.get('additional_info', '')

        if AdminAccountDetails.objects.filter(account_type=account_type).exists():
            # Prevent duplicate account types
            return redirect('admin_dashboard:edit_payment_details')

        AdminAccountDetails.objects.create(
            account_type=account_type,
            account_number=account_number,
            account_name=account_name,
            additional_info=additional_info
        )

        return redirect('admin_dashboard:edit_payment_details')

    accounts = AdminAccountDetails.objects.all()
    existing_account_types = accounts.values_list('account_type', flat=True)
    account_types = AdminAccountDetails.ACCOUNT_TYPES

    return render(request, 'admin_dashboard/edit_payment_details.html', {
        'accounts': accounts,
        'existing_account_types': existing_account_types,
        'account_types': account_types
    })


def edit_account(request, account_id):
    account = get_object_or_404(AdminAccountDetails, id=account_id)

    if request.method == 'POST':
        account.account_number = request.POST.get('account_number')
        account.account_name = request.POST.get('account_name')
        account.additional_info = request.POST.get('additional_info', '')
        account.save()

        return redirect('admin_dashboard:edit_payment_details')  # Redirect back to accounts list

    return render(request, 'admin_dashboard/edit_account.html', {'account': account})




from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import PaymentConfirmation, CustomerProfile

@staff_member_required
def view_submissions(request):
    confirmations = PaymentConfirmation.objects.all()
    profiles = CustomerProfile.objects.all()

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        profile = CustomerProfile.objects.get(id=profile_id)
        # Toggle status
        profile.status = 'active' if profile.status == 'inactive' else 'inactive'
        profile.save()
        return redirect('admin_dashboard:view_submissions')

    return render(request, 'admin_dashboard/view_submissions.html', {
        'confirmations': confirmations,
        'profiles': profiles
    })
