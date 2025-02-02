from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('terms/', views.terms, name='terms'),
    
    # Why RBS
    path('why-rbs/', views.why_rbs, name='why_rbs'),
    
    # Sector Expertise
    path('sector-expertise/', views.sector_expertise, name='sector_expertise'),
    path('sector/corporate-service-providers/', views.corporate_service_providers, name='corporate_service_providers'),
    path('sector/real-estate-finance/', views.real_estate_finance, name='real_estate_finance'),
    path('sector/private-equity/', views.private_equity, name='private_equity'),
    path('sector/asset-management/', views.asset_management, name='asset_management'),
    path('sector/private-debt/', views.private_debt, name='private_debt'),
    path('sector/infrastructure-renewables/', views.infrastructure_renewables, name='infrastructure_renewables'),
    
    # Locations
    path('locations/jersey/', views.jersey, name='jersey'),
    path('locations/guernsey/', views.guernsey, name='guernsey'),
    path('locations/gibraltar/', views.gibraltar, name='gibraltar'),
    path('locations/isle-of-man/', views.isle_of_man, name='isle_of_man'),
    path('locations/luxembourg/', views.luxembourg, name='luxembourg'),
    path('locations/london/', views.london, name='london'),
    
    # Services
    path('services/bank-accounts-overdrafts/', views.bank_accounts_overdrafts, name='bank_accounts_overdrafts'),
    path('services/cash-management/', views.cash_management, name='cash_management'),
    path('services/cards-payments/', views.cards_payments, name='cards_payments'),
    path('services/financing/', views.financing, name='financing'),
    path('services/sustainable-finance/', views.sustainable_finance, name='sustainable_finance'),
    path('services/depositary-services/', views.depositary_services, name='depositary_services'),
    
    # Where we are
    path('where-we-are/', views.where_we_are, name='where_we_are'),
    
    # Markets & Trading
    path('markets/', views.markets, name='markets'),
    path('markets/foreign-exchange/', views.foreign_exchange, name='foreign_exchange'),
    path('markets/money-market-deposits/', views.money_market_deposits, name='money_market_deposits'),
    path('markets/notice-deposits/', views.notice_deposits, name='notice_deposits'),
    
    # News & Insights
    path('insights/', views.insights, name='insights'),
    path('news/', views.news, name='news'),
    
    # Online Banking
    path('eq-online-banking/', views.eq_online_banking, name='eq_online_banking'),
    path('eq-mobile/', views.eq_mobile, name='eq_mobile'),
    path('eq-account-opening/', views.eq_account_opening, name='eq_account_opening'),
    path('eq-support/smartcard/', views.smartcard_support, name='smartcard_support'),
    path('eq-support/', views.eq_support_centre, name='eq_support_centre'),
    
    # Security & Support
    path('fraud-security/', views.fraud_security, name='fraud_security'),
    path('debit-card-support/', views.debit_card_support, name='debit_card_support'),
    path('report-fraud/', views.report_fraud, name='report_fraud'),
    path('corporate-account-reclaims/', views.corporate_account_reclaims, name='corporate_account_reclaims'),
    path('account-changes/', views.account_changes, name='account_changes'),
    
    # Information Centre
    path('results-centre/', views.results_centre, name='results_centre'),
    path('bank-base-rate/', views.bank_base_rate, name='bank_base_rate'),
    path('key-information-priips/', views.key_information_priips, name='key_information_priips'),
    path('tax-information-exchange/', views.tax_information_exchange, name='tax_information_exchange'),
    path('fees-and-charges/', views.fees_and_charges, name='fees_and_charges'),
    path('psd2/', views.psd2, name='psd2'),
    path('luxembourg-ownership/', views.luxembourg_ownership, name='luxembourg_ownership'),
    
    # Contact & Feedback
    path('contact/', views.contact, name='contact'),
    path('complaints/', views.complaints, name='complaints'),
    path('feedback/', views.feedback, name='feedback'),
    path('nominate-staff/', views.nominate_staff, name='nominate_staff'),
    path('intermediary-feedback/', views.intermediary_feedback, name='intermediary_feedback'),
    
    
] 