from locale import currency
from urllib import request
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
import requests
import xml.etree.ElementTree as ET

from dateutil.relativedelta import relativedelta

def get_courses():
    res = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req=20/02/2022')
    tree = res.text
    root = ET.fromstring(tree)
    courses=[]
    for child in root:
        courses_currency = child[1].text
        courses_course = child[4].text
        courses_course = courses_course.replace(',','.',1)
        courses.append({'rate':courses_course,'currency': courses_currency})
    return courses

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def personal_account(request):
    if request.user.id is None:
        return redirect('login')

    context = {}

    courses = get_courses()
    context['exchange_rate'] = courses


    
    default_categories = Categories.objects.select_related().filter(user_id=9)
    default_currencies = Currency.objects.select_related()
    if request.GET.get('wallet-currency'):
        cur = dict(request.GET)['wallet-currency']
    else:
        cur=list(Currency.objects.all())

    user_balances = Balances.objects.select_related().filter(user_id=request.user.id, currency_id__name__in=cur)

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
    # print(form_operation.errors["__all__"].as_data()[0].code)
    form_errors=[]
    if form_operation.errors:
        for per in form_operation.errors["__all__"].as_data():
            form_errors.append({'message':per.message,'code':per.code})
        #context['form_errors'] = form_operation.errors["__all__"].as_data()
        #print(context['form_errors'])
        context['form_errors'] = form_errors
    else:
        context['form_errors'] = []
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
    if request.GET.get('scroll-date'):
        user_balances = Balances.objects.select_related().filter(user_id=request.user.id,currency_id__name='RUB')
        smart_percent=100
        need_date = date.today()+relativedelta(months=-12-int(request.GET['scroll-date']))
        current_year = int(need_date.strftime("%Y"))
        current_month = int(need_date.strftime("%m"))-1
        for z in range(int(request.GET['scroll-date'])):
            smart_percent = smart_percent * IPC[current_month][current_year-1991]/100
            current_month=(current_month+1)%12
            if current_month == 0:
                current_year+=1

        for balance in user_balances:
            balance.amount = toFixed(balance.amount - balance.amount*Decimal((smart_percent-100)/100),2)
            
    else:
        user_balances=[]
    
    context['user_balances'] = user_balances
    balances = Balances.objects.select_related('currency_id').filter(user_id=request.user.id)
    courses=get_courses()
    result = []
    all_amount = 0
    for i in balances:
        for z in courses:
            if str(z['currency']) == str(i.currency_id):
                ch = float(i.amount) * float(z['rate'])
                result.append([str(i.currency_id), ch])
                # print(str(i.currency_id))
                # print(float(i.amount/z[i.currency_id]))
                all_amount += float(i.amount) * float(z['rate'])
                break
        else:
            result.append(['RUB', float(i.amount)])
            all_amount +=float(i.amount)
    answer=[]
    for i in result:
        answer.append([i[0], i[1] / all_amount*100])
    # print(answer)
    context['exchanged_balances']= answer
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
    if request.GET.get('wallet-type')=='??????????????':
        operation_type = '-'
    else:
        operation_type = '+'
    example_income_data = Operations.objects.select_related().filter(
        user_id=request.user.id,
        operation_type=operation_type,
        datetime__range=date_range,
        currency=currency
    ).values('datetime').annotate(total=Sum('amount'))
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
        if len(days) != 1:
            coefficients = estimate_coefficients(days, outlays)
            amount = 0.0
            start_day, end_day = min(days), monthrange(datetime.now().year, int(month))
            
            for i in range(start_day, end_day[1] + 1):
                amount += coefficients[1] * i + coefficients[0]
        else:
            amount = outlays[0]
            
        context['monthly_outlay_data'] = data_formatted
        context['expected_outlay'] = toFixed(amount, 2)
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

