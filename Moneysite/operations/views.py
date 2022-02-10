from django.shortcuts import render

from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm


def personal_account(request):
    context = {}

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id)
    default_categories = Categories.objects.select_related().filter(user_id=9)

    context['balance'] = user_balances
    context['categories'] = default_categories

    if request.method == 'POST':  
        form = AddOperationForm(request.POST)
        context['form'] = form
    
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            print('here22')
    else:
        form = AddOperationForm()
        context['form'] = form
        
        print('here1')
    
    return render(request, 'manager.html', context)


def example(request):
    context = {}
    return render(request, 'LK.html', context)


def example_stat(request):
    context = {}
    return render(request, 'LK_statistics.html', context)
