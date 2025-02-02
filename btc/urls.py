from django.urls import path
from . import views

app_name = 'btc'

urlpatterns = [
    path('transactions/', views.user_btc_transactions, name='user_transactions'),
]