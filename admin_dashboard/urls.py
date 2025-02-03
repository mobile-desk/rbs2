from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.user_list, name='user_list'),

    path('change-user-password/<int:user_id>/', views.change_user_password, name='change_user_password'),

    path('edit-verification-codes/', views.edit_verification_codes, name='edit_verification_codes'),
    path('verification-status-control/', views.verification_status_control, name='verification_status_control'),
    path('edit-config/', views.edit_config, name='edit_config'),
    
    path('users/<int:user_id>/make-admin/', views.make_admin, name='make_admin'),
    path('users/<int:user_id>/remove-admin/', views.remove_admin, name='remove_admin'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/create/', views.create_user, name='create_user'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transaction/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),

    path('users/<int:user_id>/modify-balance/', views.modify_balance, name='modify_balance'),

    
    path('send-mail/', views.send_mail_to_user, name='send_mail'),
    path('send-direct-email/', views.send_direct_email, name='send_direct_email'),
    path('login/', views.admin_login, name='admin_login'),



    path('passports/', views.manage_passports, name='manage_passports'),
    path('passports/add/', views.add_edit_passport, name='add_passport'),
    path('passports/edit/<int:user_id>/', views.add_edit_passport, name='edit_passport'),
    path('passports/delete/<int:user_id>/', views.delete_passport, name='delete_passport'),
    path('passports/download/<int:user_id>/', views.download_passport, name='download_passport'),

    path('btc-wallets/', views.list_btc_wallets, name='list_btc_wallets'),
    path('btc-wallets/create/', views.create_btc_wallet, name='create_btc_wallet'),
    path('btc-wallets/edit/<int:wallet_id>/', views.edit_btc_wallet, name='edit_btc_wallet'),
    path('btc-status-control/', views.btc_status_control, name='btc_status_control'),


    path('edit-payment-details/', views.edit_payment_details, name='edit_payment_details'),
    path('edit/<int:account_id>/', views.edit_account, name='edit_account'),

    
]