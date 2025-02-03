from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CardApplicationForm
from .models import CardApplication

from users.models import CustomerProfile


@login_required
def home(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    return render(request, 'cards/home.html')

@login_required
def apply_for_card(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    if request.method == 'POST':
        form = CardApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('cards:card_application_success')
    else:
        form = CardApplicationForm()
    return render(request, 'cards/apply.html', {'form': form})

@login_required
def card_application_success(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    return render(request, 'cards/success.html')

@login_required
def my_applications(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if profile.status == 'inactive':
        return redirect('authenticating:initial_deposit')
    
    applications = CardApplication.objects.filter(user=request.user)
    return render(request, 'cards/my_applications.html', {'applications': applications})