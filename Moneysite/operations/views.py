from locale import currency
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractDay
from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm
from django.db.models.functions import TruncDay
from datetime import date, datetime
from datetime import timedelta
from json import dumps
from .currency_exchange_rate_parsing.parsing import CurrencyConverter
import itertools
from calendar import monthrange
import numpy as np
from decimal import Decimal
from .IPC import IPC

from dateutil.relativedelta import relativedelta


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def personal_account(request):
    if request.user.id is None:
        return redirect('login')

    context = {}

    test=Balances.objects.select_related().filter(currency_id__name='ABC')
    for i in test:
        print(type(i.amount))
    
    default_categories = Categories.objects.select_related().filter(user_id=9)
    default_currencies = Currency.objects.select_related()
    # print(dict(request.GET)['wallet-currency'])
    if request.GET.get('wallet-currency'):
        cur = dict(request.GET)['wallet-currency']
    else:
        cur=list(Currency.objects.all())

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id,currency_id__name__in=cur)
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

    
    month = request.GET.get('outlay-month-select') if request.GET.get('outlay-month-select') else datetime.now().month
    monthly_outlay_data = Operations.objects.select_related().filter(
        user_id=request.user.id, 
        operation_type='-'
    ).annotate(
        month=ExtractMonth('datetime'), 
        day=ExtractDay('datetime')
    ).values('month', 'day', 'amount').filter(
        month=month
    )

    example_outlay_data = Operations.objects.select_related().filter(
        user_id=request.user.id, 
        operation_type='-',
        datetime__range=[
            date.today() - timedelta(days=30),
            date.today()
        ]
    ).values('datetime').annotate(total=Sum('amount'))
    # infliation = 0.06
    if request.GET.get('scroll-date'):
        user_balances = Balances.objects.select_related().filter(user_id=request.user.id,currency_id__name='RUB')
        smart_percent=100
        need_date = date.today()+relativedelta(months=-12-int(request.GET['scroll-date']))
        current_year = int(need_date.strftime("%Y"))
        current_month = int(need_date.strftime("%m"))-1
        print(current_month, current_year)
        # if current_year!=date.today().strftime("%Y"):
        for z in range(int(request.GET['scroll-date'])):
            smart_percent = smart_percent * IPC[current_month][current_year-1991]/100
            current_month=(current_month+1)%12
            if current_month == 0:
                current_year+=1
        # while current_month<12:
            
        # for i in range(scroll_date_range):
        print(smart_percent)
        for balance in user_balances:
            print(balance.amount*Decimal((smart_percent-100)/100))
            balance.amount = toFixed(balance.amount - balance.amount*Decimal((smart_percent-100)/100),2)
            
    else:
        user_balances=[]
    
    context['user_balances'] = user_balances

    example_budget_data = []
    if request.GET.get('wallet-start-date') and request.GET.get('wallet-end-date'):
        date_range=[request.GET['wallet-start-date'],
                request.GET['wallet-end-date']]
    else:
        date_range=[date.today() - timedelta(days=30),
               date.today()]
    if request.GET.get('wallet-currency'):
        currency = request.GET['wallet-currency']
    else:
        currency = 'RUB'
    if request.GET.get('wallet-type')=='Расходы':
        operation_type = '-'
    else:
        operation_type = '+'
    example_income_data = Operations.objects.select_related().filter(
        user_id=request.user.id,
        operation_type=operation_type,
        datetime__range=date_range,
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
        days.append(int(elem['day']))
        outlays.append(amount)

    if days:
        coefficients = estimate_coefficients(days, outlays)
        amount = 0.0
        start_day, end_day = min(days), max(days) #monthrange(int(datetime.now().year), month)
        
        for i in range(start_day, end_day + 1):
            amount += coefficients[1] * i + coefficients[0]

        context['monthly_outlay_data'] = data_formatted
        context['expected_outlay'] = amount
        context['outlay_data_flag'] = True
    else:
        context['outlay_data_flag'] = False
        context['monthly_outlay_data'] = [[0, 0]]

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

    return [b_0, b_1]

