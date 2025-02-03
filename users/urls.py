from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    
    path('initial-deposit/', views.initial_deposit, name='initial_deposit'),
    path('payment-selection/', views.payment_selection, name='payment_selection'),
    path('payment-details/<str:payment_type>/', views.get_payment_details, name='payment_details'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),


    path('register/', views.register_step1, name='register_step1'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('register/step3/', views.register_step3, name='register_step3'),
    path('register/step4/', views.register_step4, name='register_step4'),


    path('login/', views.user_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
    path('account/<int:account_id>/transactions/', views.account_transactions, name='account_transactions'),
    path('account/<int:account_id>/transactions/download/', views.download_transactions_csv, name='download_transactions_csv'),
    #path('account/<int:account_id>/transactions/download_pdf/', views.download_transactions_pdf, name='download_transactions_pdf'),

    path('profile/', views.profile_view, name='profile'),
    path('mailbox/', views.mailbox_list, name='mailbox_list'),
    path('mailbox/<int:message_id>/', views.mailbox_detail, name='mailbox_detail'),

    path('account-settings/', views.account_settings, name='account_settings'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Add this line


]

