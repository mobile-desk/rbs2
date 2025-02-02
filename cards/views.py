from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CardApplication
from django.urls import reverse

@login_required
def apply_card(request):
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        
        # Check if user has pending applications
        if CardApplication.objects.filter(user=request.user, status='PENDING').exists():
            messages.error(request, 'You already have a pending card application.')
            return redirect('cards:application_list')
        
        application = CardApplication.objects.create(
            user=request.user,
            card_type=card_type
        )
        messages.success(request, 'Card application submitted successfully!')
        return redirect('cards:application_detail', pk=application.pk)
    
    return render(request, 'cards/apply_card.html', {
        'card_choices': CardApplication.CARD_CHOICES
    })

@login_required
def application_list(request):
    applications = CardApplication.objects.filter(user=request.user)
    return render(request, 'cards/application_list.html', {
        'applications': applications
    })

@login_required
def application_detail(request, pk):
    application = get_object_or_404(CardApplication, pk=pk, user=request.user)
    return render(request, 'cards/application_detail.html', {
        'application': application
    })