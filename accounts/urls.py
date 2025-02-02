from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView


app_name = 'authenticating'

urlpatterns = [
    path('pre-login', views.login, name="prelogin"),
    path('dashboard', views.dashboard, name="dashboard"),
    
    
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

]