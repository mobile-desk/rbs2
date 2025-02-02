from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('apply/', views.apply_card, name='apply_card'),
    path('applications/', views.application_list, name='application_list'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
]