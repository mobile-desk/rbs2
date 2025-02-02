from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CardApplicationForm
from .models import CardApplication



@login_required
def home(request):
    return render(request, 'cards/home.html')

@login_required
def apply_for_card(request):
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
    return render(request, 'cards/success.html')

@login_required
def my_applications(request):
    applications = CardApplication.objects.filter(user=request.user)
    return render(request, 'cards/my_applications.html', {'applications': applications})