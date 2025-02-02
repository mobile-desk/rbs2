from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    path('pat/', views.pat, name='pat'),
    path('transaction-list/', views.transaction_list, name='transaction_list'),
    path('submit-payment/', views.submit_payment, name='submit_payment'),
    path('verify-tax-code/', views.verify_tax_code, name='verify_tax_code'),
    path('verify-imf-code/', views.verify_imf_code, name='verify_imf_code'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('verify-anti-terrorist-code/', views.verify_anti_terrorist_code, name='verify_anti_terrorist_code'),
    path('verify-anti-money-laundering-code/', views.verify_anti_money_laundering_code, name='verify_anti_money_laundering_code'),



    path('process-transaction/', views.process_transaction, name='process_transaction'),
    path('transaction-success/', views.transaction_success, name='transaction_success'),
    path('receipt/<uuid:receipt_id>/', views.display_receipt, name='display_receipt'),

    path('international-transfer/', views.create_international_transfer, name='create_international_transfer'),
    path('transfer-success/', views.transfer_success, name='transfer_success'),
]
