from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractDay
from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm
from django.db.models.functions import TruncDay
from datetime import date
from datetime import timedelta
from json import dumps
from .currency_exchange_rate_parsing.parsing import CurrencyConverter
import itertools
import numpy as np


def personal_account(request):
    if request.user.id is None:
        return redirect('login')

    context = {}

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id)
    default_categories = Categories.objects.select_related().filter(user_id=9)
    default_currencies = Currency.objects.select_related()

    # for balance in user_balances:
    #    print(balance.currency_id)
    # print(CurrencyConverter.get_currency_exchange_rate('dollar', 'ruble'))
    if request.method == 'GET' and 'start-date' in request.GET:
        user_operations = Operations.objects.select_related().filter(
            user_id=request.user.id,
            datetime__range=[
                request.GET['start-date'],
                request.GET['end-date']
        ]).order_by('-datetime')
    else:
        user_operations = Operations.objects.select_related().filter(
            user_id=request.user.id
        ).order_by('-datetime')

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
    if request.user.id is None:
        return redirect('login')
    context = {}

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id)
    context['user_balances'] = user_balances

    monthly_outlay_data = Operations.objects.select_related().filter(
        user_id=request.user.id, 
        operation_type='-'
    ).annotate(month=ExtractMonth('datetime'), day=ExtractDay('datetime')).values('month', 'day', 'amount').filter(month=2)

    example_outlay_data = Operations.objects.select_related().filter(
        user_id=request.user.id, 
        operation_type='-',
        datetime__range=[
            date.today() - timedelta(days=30),
            date.today()
        ]
    ).values('datetime').annotate(total=Sum('amount'))

    example_budget_data = []
    if request.GET.get('wallet-start-date') and request.GET.get('wallet-end-date'):
        range=[request.GET['wallet-start-date'],
                request.GET['wallet-end-date']]
    else:
        range=[date.today() - timedelta(days=30),
               date.today()]
    if request.GET.get('wallet-currency'):
        currency = request.GET['wallet-currency']
    else:
        currency = 'RUB'
    if request.GET.get('wallet-type')=='Расходы':
        type = '-'
    else:
        type = '+'
    example_income_data = Operations.objects.select_related().filter(
        user_id=request.user.id,
        operation_type=type,
        datetime__range=range,
        currency=currency
    ).values('datetime').annotate(total=Sum('amount'))
    '''if 'currency' in request.GET:
        example_category_data= Operations.objects.select_related('category__category_name').filter(
            user_id=request.user.id,
            operation_type='-',
            datetime__range=[
                date.today() - timedelta(days=30),
                date.today()
            ],
            currency=request.GET['currency']
        ).values('category__category_name').annotate(total=Sum('amount'))
        print(example_category_data)
        print(1)
    else:'''
    if request.GET.get('category-start-date') and request.GET.get('category-end-date'):
        category_daterange = [request.GET['category-start-date'],
                 request.GET['category-end-date']]
    else:
        category_daterange = [date.today() - timedelta(days=30),
                 date.today()]
    if request.GET.get('category-currency'):
        category_currency = request.GET['category-currency']
    else:
        category_currency = request.user.displayed_currency
    example_category_data = Operations.objects.select_related('category__category_name').filter(
        user_id=request.user.id,
        operation_type='-',
        datetime__range=category_daterange,
        currency=category_currency
    ).values('category__category_name').annotate(total=Sum('amount'))
        # print(example_category_data)

    data_formatted = []
    for elem in example_income_data:
        data_formatted.append([elem['datetime'].strftime("%Y-%m-%d"), float(elem['total'])])

    context['data_income'] = data_formatted

    data_formatted = []
    for elem in example_outlay_data:
        data_formatted.append([elem['datetime'].strftime("%Y-%m-%d"), float(elem['total'])])

    context['data_outlay'] = data_formatted

    data_formatted = []
    for elem in example_category_data:
        data_formatted.append([elem['category__category_name'], float(elem['total'])])

    context['data_categories'] = data_formatted

    data_formatted = []
    days = []
    outlays = []
    amount = 0.0
    for elem in monthly_outlay_data:
        amount += float(elem['amount'])
        data_formatted.append([elem['day'], amount])
        days.append(elem['day'])
        outlays.append(amount)

    coefficients = estimate_coefficients(days, outlays)
    context['monthly_outlay_data'] = data_formatted
    context['coefficients'] = coefficients
    # print(coefficients)

    context['data_budget'] = example_budget_data

    return render(request, 'LK_stats.html', context)

def estimate_coefficients(list_x, list_y):
    x = np.array(list_x)
    y = np.array(list_y)

    n = np.size(x)
    mean_x, mean_y = np.mean(x), np.mean(y) 

    SS_xy = np.sum(y * x - n * mean_y * mean_x) 
    SS_xx = np.sum(x * x - n * mean_x * mean_x) 

    b_1 = SS_xy / SS_xx 
    b_0 = mean_y - b_1 * mean_x 

    return [[0, b_0], [31, b_0 + 31 * b_0]]

