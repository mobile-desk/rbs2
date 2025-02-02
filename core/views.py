from django.shortcuts import render

#
#  Home
def home(request):
    return render(request, 'core/home.html')


def about_us(request):
    return render(request, 'core/about.html')


def terms(request):
    return render(request, 'core/terms.html')


#
# Why RBS
def why_rbs(request):
    custom_path = "why/"
    return render(request, 'core/why_rbs.html', {"custom_path": custom_path})

# Sector Expertise
def sector_expertise(request):
    return render(request, 'core/sector_expertise.html')

#
def corporate_service_providers(request):
    return render(request, 'core/corporate_service_providers.html')

def real_estate_finance(request):
    return render(request, 'core/real_estate_finance.html')

def private_equity(request):
    return render(request, 'core/private_equity.html')

def asset_management(request):
    return render(request, 'core/asset_management.html')

def private_debt(request):
    return render(request, 'core/private_debt.html')

def infrastructure_renewables(request):
    return render(request, 'core/infrastructure_renewables.html')

# Locations
def jersey(request):
    return render(request, 'core/locations/jersey.html')

def guernsey(request):
    return render(request, 'core/locations/guernsey.html')

def gibraltar(request):
    return render(request, 'core/locations/gibraltar.html')

def isle_of_man(request):
    return render(request, 'core/locations/isle_of_man.html')

def luxembourg(request):
    return render(request, 'core/locations/luxembourg.html')

def london(request):
    return render(request, 'core/locations/london.html')

# Services
def bank_accounts_overdrafts(request):
    return render(request, 'core/services/bank_accounts_overdrafts.html')

def cash_management(request):
    return render(request, 'core/services/cash_management.html')

def cards_payments(request):
    return render(request, 'core/services/cards_payments.html')

def financing(request):
    return render(request, 'core/services/financing.html')

def sustainable_finance(request):
    return render(request, 'core/services/sustainable_finance.html')

def depositary_services(request):
    return render(request, 'core/services/depositary_services.html')

# Where we are
def where_we_are(request):
    return render(request, 'core/where_we_are.html')

# Markets & Trading
def markets(request):
    return render(request, 'core/markets/markets.html')

def foreign_exchange(request):
    return render(request, 'core/markets/foreign_exchange.html')

def money_market_deposits(request):
    return render(request, 'core/markets/money_market_deposits.html')

def notice_deposits(request):
    return render(request, 'core/markets/notice_deposits.html')

# News & Insights
def insights(request):
    return render(request, 'core/insights.html')

def news(request):
    return render(request, 'core/news.html')

# Online Banking
def eq_online_banking(request):
    return render(request, 'core/online_banking/eq_online_banking.html')

def eq_mobile(request):
    return render(request, 'core/online_banking/eq_mobile.html')

def eq_account_opening(request):
    return render(request, 'core/online_banking/eq_account_opening.html')

def smartcard_support(request):
    return render(request, 'core/online_banking/smartcard_support.html')

def eq_support_centre(request):
    return render(request, 'core/online_banking/eq_support_centre.html')

# Security & Support
def fraud_security(request):
    return render(request, 'core/security/fraud_security.html')

def debit_card_support(request):
    return render(request, 'core/security/debit_card_support.html')

def report_fraud(request):
    return render(request, 'core/security/report_fraud.html')

def corporate_account_reclaims(request):
    return render(request, 'core/security/corporate_account_reclaims.html')

def account_changes(request):
    return render(request, 'core/security/account_changes.html')

# Information Centre
def results_centre(request):
    return render(request, 'core/information/results_centre.html')

def bank_base_rate(request):
    return render(request, 'core/information/bank_base_rate.html')

def key_information_priips(request):
    return render(request, 'core/information/key_information_priips.html')

def tax_information_exchange(request):
    return render(request, 'core/information/tax_information_exchange.html')

def fees_and_charges(request):
    return render(request, 'core/information/fees_and_charges.html')

def psd2(request):
    return render(request, 'core/information/psd2.html')

def luxembourg_ownership(request):
    return render(request, 'core/information/luxembourg_ownership.html')

# Contact & Feedback
def contact(request):
    return render(request, 'core/contact/contact.html')

def complaints(request):
    return render(request, 'core/contact/complaints.html')

def feedback(request):
    return render(request, 'core/contact/feedback.html')

def nominate_staff(request):
    return render(request, 'core/contact/nominate_staff.html')

def intermediary_feedback(request):
    return render(request, 'core/contact/intermediary_feedback.html')



