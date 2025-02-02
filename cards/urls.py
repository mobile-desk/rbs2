from django.urls import path
from . import views


app_name = 'cards'

urlpatterns = [
    path('apply/', views.apply_for_card, name='apply_for_card'),
    path('success/', views.card_application_success, name='card_application_success'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('', views.home, name='home'),
]