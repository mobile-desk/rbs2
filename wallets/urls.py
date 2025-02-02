from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('account/create/', views.create_account, name='create_account'),
    path('accounts/', views.account_list, name='account_list'),
    path('account/<int:pk>/', views.account_detail, name='account_detail'),
]