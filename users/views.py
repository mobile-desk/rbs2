from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from transactions.models import Transaction
from django.contrib.auth.models import User
from .forms import CustomerTypeForm, PersonalCustomerForm, BusinessCustomerForm, CreditCardCustomerForm, MortgageCustomerForm, AccountSetupForm, PinPasswordForm
import random
from .models import CustomerProfile, Mailbox
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.units import inch
import io
import os
from django.conf import settings

from reportlab.lib.utils import ImageReader


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserSettingsForm, CustomerProfileForm
from accounts.models import Passport, BTCWallet, Account


from core.models import NSiteSettings



def register_step1(request):
    if request.user.is_authenticated:
        return redirect('authenticating:dashboard')

    if request.method == 'POST':
        form = CustomerTypeForm(request.POST)
        if form.is_valid():
            customer_type = form.cleaned_data['customer_type']
            request.session['customer_type'] = customer_type
            return redirect('authenticating:register_step2')
    else:
        form = CustomerTypeForm()
    return render(request, 'users/register_step1.html', {'form': form})



def register_step2(request):
    customer_type = request.session.get('customer_type')
    if customer_type == 'personal':
        form_classes = [PersonalCustomerForm]
    elif customer_type == 'business':
        form_classes = [PersonalCustomerForm, BusinessCustomerForm]
    elif customer_type == 'credit_card':
        form_classes = [PersonalCustomerForm, CreditCardCustomerForm]
    elif customer_type == 'mortgage':
        form_classes = [PersonalCustomerForm, MortgageCustomerForm]
    else:
        return redirect('authenticating:register_step1')

    if request.method == 'POST':
        forms = [form_class(request.POST, request.FILES) for form_class in form_classes]
        if all(form.is_valid() for form in forms):
            customer_info = {}
            for form in forms:
                customer_info.update(form.cleaned_data)

            if 'date_of_birth' in customer_info:
                customer_info['date_of_birth'] = customer_info['date_of_birth'].isoformat()

            if 'passport' in request.FILES:
                passport_image = request.FILES['passport']
                request.session['passport_image'] = passport_image.name

                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
                os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist

                temp_path = os.path.join(temp_dir, passport_image.name)
                with open(temp_path, 'wb+') as destination:
                    for chunk in passport_image.chunks():
                        destination.write(chunk)

            request.session['customer_info'] = customer_info
            return redirect('authenticating:register_step3')
    else:
        forms = [form_class() for form_class in form_classes]

    return render(request, 'users/register_step2.html', {'forms': forms})

def register_step3(request):
    if request.method == 'POST':
        form = AccountSetupForm(request.POST)
        if form.is_valid():
            request.session['account_setup'] = form.cleaned_data
            if form.cleaned_data['know_pin'] == 'yes':
                return redirect('authenticating:register_step4')
            else:
                return redirect('register_step4')
    else:
        customer_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        form = AccountSetupForm(initial={'customer_number': customer_number})
    return render(request, 'users/register_step3.html', {'form': form})

def register_step4(request):
    if request.method == 'POST':
        form = PinPasswordForm(request.POST)
        if form.is_valid():
            customer_info = request.session['customer_info']
            account_setup = request.session['account_setup']
            email = customer_info['email']
            password = form.cleaned_data['password']
            customer_number = account_setup['customer_number']

            user = User.objects.create_user(
                username=customer_number,
                email=email,
                password=password
            )
            user.first_name = customer_info['first_name']
            user.last_name = customer_info['last_name']
            user.save()

            CustomerProfile.objects.create(
                user=user,
                customer_type=request.session['customer_type'],
                middle_name=customer_info.get('middle_name'),
                date_of_birth=customer_info['date_of_birth'],
                postcode=customer_info.get('postcode'),
                business_postcode=customer_info.get('business_postcode'),
                customer_number=account_setup['customer_number'],
                pin=form.cleaned_data['pin']
            )

            if 'passport_image' in request.session:
                passport_image_name = request.session['passport_image']
                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', passport_image_name)
                with open(temp_path, 'rb') as f:
                    Passport.objects.create(
                        user=user,
                        passport_number='Temporary',
                        issue_date=timezone.now().date(),
                        expiry_date=timezone.now().date() + timezone.timedelta(days=3650),
                        country_of_issue='Temporary',
                        passport_image=File(f, name=passport_image_name)
                    )
                os.remove(temp_path)
                del request.session['passport_image']

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

            login(request, user)
            return redirect('authenticating:dashboard')
    else:
        form = PinPasswordForm()
    return render(request, 'users/register_step4.html', {'form': form})




def user_login(request):
    if request.user.is_authenticated:
        return redirect('authenticating:dashboard')

    if 'step' in request.GET and request.GET['step'] == '2':
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('authenticating:dashboard')
            else:
                return render(request, 'users/login2.html', {'error': 'Invalid email or password'})
        return render(request, 'users/login2.html')
    else:
        return render(request, 'users/login.html')




'''def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid email or password'})
    return render(request, 'users/login.html')

'''


@login_required
def dashboard(request):
    user = request.user
    accounts = Account.objects.filter(user=user)
    last_login = user.last_login


    btc_active = NSiteSettings.objects.filter(user=request.user).first().btc_active if NSiteSettings.objects.filter(user=request.user).exists() else True

    try:
        # Fetch the BTCWallet associated with the logged-in user
        btc_wallet = BTCWallet.objects.get(user=user)
    except BTCWallet.DoesNotExist:
        # Handle the case where no wallet exists for the user
        btc_wallet = None






    if request.method == 'POST':
        from_account = Account.objects.get(id=request.POST['from_account'])
        to_account_number = request.POST['to_account']
        #amount = float(request.POST['amount'])
        amount = Decimal(request.POST['amount'])

        try:
            to_account = Account.objects.get(account_number=to_account_number)
        except Account.DoesNotExist:
            messages.error(request, 'Recipient account not found.')
            return redirect('authenticating:dashboard')

        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            Transaction.objects.create(
                account=from_account,
                amount=amount,
                transaction_type='Debit',
                description=f'Transfer to account {to_account.account_number}',
                timestamp=timezone.now()
            )

            # Create a corresponding transaction for the receiving account
            Transaction.objects.create(
                account=to_account,
                amount=amount,
                transaction_type='Credit',
                description=f'Received from account {from_account.account_number}',
                timestamp=timezone.now()
            )

            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds.')

    context = {
        'accounts': accounts,
        'last_login': last_login,
        'btc_wallet': btc_wallet,
        'btc_active': btc_active,
    }

    return render(request, 'users/dashboard.html', context)







'''
@login_required
def edit_profile(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('authenticating:profile')  # Redirect to the profile page after saving
    else:
        form = CustomerProfileForm(instance=profile)

    context = {
        'form': form,
        'name': request.user.get_full_name(),
        'email': request.user.email,
        'date_joined': request.user.date_joined,
    }
    return render(request, 'users/edit_profile.html', context)

'''






@login_required
def edit_profile(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save user first and last name
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()

            # Save profile
            form.save()
            return redirect('authenticating:profile')  # Redirect to the profile page after saving
    else:
        form = CustomerProfileForm(instance=profile)

    context = {
        'form': form,
        'user': request.user,  # Pass the user object to the template
    }
    return render(request, 'users/edit_profile.html', context)








@login_required
def profile_view(request):
    # Fetch the profile for the logged-in user
    profile = get_object_or_404(CustomerProfile, user=request.user)
    user = request.user

    accounts = Account.objects.filter(user=user)

    passport = Passport.objects.filter(user=user).first()


    # Prepare context for the template
    context = {
        'name': request.user.get_full_name(),  # Fetch the user's full name
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'customer_type': profile.customer_type,
        'middle_name': profile.middle_name,
        'date_of_birth': profile.date_of_birth,
        'address': profile.postcode,
        'business_postcode': profile.business_postcode,
        'customer_number': profile.customer_number,
        'profile': profile,
        'accounts': accounts,
        'passport': passport

    }

    return render(request, 'users/profile.html', context)





@login_required
def account_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    context = {
        'account': account,
        'transactions': transactions,
    }

    return render(request, 'users/account_transactions.html', context)



@login_required
def download_transactions_csv(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="transactions_{account.account_number}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Amount', 'Type'])

    for transaction in transactions:
        writer.writerow([transaction.timestamp, transaction.description, transaction.amount, transaction.transaction_type])

    return response


'''
@login_required
def download_transactions_pdf(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transactions_{account.account_number}.pdf"'

    # Create the PDF object using ReportLab
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # Convert SVG to PNG
    svg_path = "static/img/logo1.svg"
    png_image = io.BytesIO()
    cairosvg.svg2png(url=svg_path, write_to=png_image)
    png_image.seek(0)
    logo = Image(ImageReader(png_image), width=2 * inch, height=2 * inch)
    logo.hAlign = 'LEFT'
    elements.append(logo)

    # Add a title
    styles = getSampleStyleSheet()
    title = Paragraph(f"Transaction History for Account {account.account_number}", styles['Title'])
    elements.append(title)

    # Add some space
    elements.append(Paragraph("<br/>", styles['Normal']))

    # Create table data
    data = [['Date', 'Description', 'Amount', 'Type']]
    for transaction in transactions:
        data.append([
            transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            transaction.description,
            f"€ {transaction.amount}",
            transaction.transaction_type,
        ])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)

    return response

'''


def home(request):
    return render(request, 'users/home.html')



def user_logout(request):
    logout(request)
    return redirect('core:home')






@login_required
def mailbox_list(request):
    messages = Mailbox.objects.filter(recipient=request.user).order_by('-date')
    return render(request, 'users/mailbox_list.html', {'messages': messages})

@login_required
def mailbox_detail(request, message_id):
    message = get_object_or_404(Mailbox, id=message_id, recipient=request.user)
    if not message.read:
        message.read = True
        message.save()
    return render(request, 'users/mailbox_detail.html', {'message': message})




@login_required
def account_settings(request):
    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'update_profile' in request.POST and user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your account settings have been updated.')
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        return redirect('users:account_settings')
    else:
        user_form = UserSettingsForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'users/account_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })




