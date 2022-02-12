from django.shortcuts import render, redirect

from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm
from django.db.models.functions import TruncDay

from .currency_exchange_rate_parsing.parsing import CurrencyConverter

def personal_account(request):
    context = {}

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id)
    default_categories = Categories.objects.select_related().filter(user_id=9)
    default_currencies = Currency.objects.select_related()

    # for balance in user_balances:
    #     print(balance.currency_id)
    # print(CurrencyConverter.get_currency_exchange_rate('dollar', 'ruble'))
    if request.method =='GET' and 'start-date' in request.GET:
        user_operations = Operations.objects.select_related().filter(user_id=request.user.id, datetime__range=[request.GET['start-date'], request.GET['end-date']]).order_by('-datetime')
    else:
        user_operations = Operations.objects.select_related().filter(user_id=request.user.id).order_by('-datetime')

    context['balance'] = user_balances
    context['currencies'] = default_currencies
    context['categories'] = default_categories
    context['operations'] = user_operations

    if request.method == 'POST':

        form_operation = AddOperationForm(request.user, request.POST)
        context['form'] = form_operation
    
        if form_operation.is_valid():
            data = form_operation.save(commit=False)
            data.user = request.user
            data.save()

            return redirect('LK')
            
    else:
        form_operation = AddOperationForm(request.user)
        context['form'] = form_operation
    
    return render(request, 'manager.html', context)


def example(request):
    context = {}
    return render(request, 'LK.html', context)


def example_stat(request):
    context = {}
    return render(request, 'LK_statistics.html', context)

def stats(request):
    context = {}
    return render(request, 'LK_stats.html', context)