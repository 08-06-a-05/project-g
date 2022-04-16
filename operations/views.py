from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractDay
from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm
from datetime import date, datetime
from datetime import timedelta
from calendar import monthrange
import numpy as np
from decimal import Decimal
from .IPC import IPC
import requests
import xml.etree.ElementTree as ET
import xlwt

from dateutil.relativedelta import relativedelta


def get_courses():
    # res = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req='+date.today().strftime("%d/%m/%Y"))
    # tree = res.text
    # print('https://www.cbr.ru/scripts/XML_daily.asp?date_req='+date.today().strftime("%d/%m/%Y"))
    # print(tree)
    # root = ET.fromstring(tree)
    # root=''
    tree='<?xml version="1.0" encoding="windows-1251"?><ValCurs Date="16.04.2022" name="Foreign Currency Market"><Valute ID="R01010"><NumCode>036</NumCode><CharCode>AUD</CharCode><Nominal>1</Nominal><Name>Австралийский доллар</Name><Value>59,6966</Value></Valute><Valute ID="R01020A"><NumCode>944</NumCode><CharCode>AZN</CharCode><Nominal>1</Nominal><Name>Азербайджанский манат</Name><Value>47,0845</Value></Valute><Valute ID="R01035"><NumCode>826</NumCode><CharCode>GBP</CharCode><Nominal>1</Nominal><Name>Фунт стерлингов Соединенного королевства</Name><Value>104,3610</Value></Valute><Valute ID="R01060"><NumCode>051</NumCode><CharCode>AMD</CharCode><Nominal>100</Nominal><Name>Армянских драмов</Name><Value>16,9786</Value></Valute><Valute ID="R01090B"><NumCode>933</NumCode><CharCode>BYN</CharCode><Nominal>1</Nominal><Name>Белорусский рубль</Name><Value>28,3060</Value></Valute><Valute ID="R01100"><NumCode>975</NumCode><CharCode>BGN</CharCode><Nominal>1</Nominal><Name>Болгарский лев</Name><Value>44,5182</Value></Valute><Valute ID="R01115"><NumCode>986</NumCode><CharCode>BRL</CharCode><Nominal>1</Nominal><Name>Бразильский реал</Name><Value>16,9746</Value></Valute><Valute ID="R01135"><NumCode>348</NumCode><CharCode>HUF</CharCode><Nominal>100</Nominal><Name>Венгерских форинтов</Name><Value>23,2166</Value></Valute><Valute ID="R01200"><NumCode>344</NumCode><CharCode>HKD</CharCode><Nominal>1</Nominal><Name>Гонконгский доллар</Name><Value>10,2240</Value></Valute><Valute ID="R01215"><NumCode>208</NumCode><CharCode>DKK</CharCode><Nominal>1</Nominal><Name>Датская крона</Name><Value>11,6509</Value></Valute><Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal><Name>Доллар США</Name><Value>80,0437</Value></Valute><Valute ID="R01239"><NumCode>978</NumCode><CharCode>EUR</CharCode><Nominal>1</Nominal><Name>Евро</Name><Value>87,0715</Value></Valute><Valute ID="R01270"><NumCode>356</NumCode><CharCode>INR</CharCode><Nominal>10</Nominal><Name>Индийских рупий</Name><Value>10,5625</Value></Valute><Valute ID="R01335"><NumCode>398</NumCode><CharCode>KZT</CharCode><Nominal>100</Nominal><Name>Казахстанских тенге</Name><Value>17,8593</Value></Valute><Valute ID="R01350"><NumCode>124</NumCode><CharCode>CAD</CharCode><Nominal>1</Nominal><Name>Канадский доллар</Name><Value>63,5217</Value></Valute><Valute ID="R01370"><NumCode>417</NumCode><CharCode>KGS</CharCode><Nominal>100</Nominal><Name>Киргизских сомов</Name><Value>98,3350</Value></Valute><Valute ID="R01375"><NumCode>156</NumCode><CharCode>CNY</CharCode><Nominal>1</Nominal><Name>Китайский юань</Name><Value>12,5630</Value></Valute><Valute ID="R01500"><NumCode>498</NumCode><CharCode>MDL</CharCode><Nominal>10</Nominal><Name>Молдавских леев</Name><Value>43,3771</Value></Valute><Valute ID="R01535"><NumCode>578</NumCode><CharCode>NOK</CharCode><Nominal>10</Nominal><Name>Норвежских крон</Name><Value>90,5554</Value></Valute><Valute ID="R01565"><NumCode>985</NumCode><CharCode>PLN</CharCode><Nominal>1</Nominal><Name>Польский злотый</Name><Value>18,6686</Value></Valute><Valute ID="R01585F"><NumCode>946</NumCode><CharCode>RON</CharCode><Nominal>1</Nominal><Name>Румынский лей</Name><Value>17,5139</Value></Valute><Valute ID="R01589"><NumCode>960</NumCode><CharCode>XDR</CharCode><Nominal>1</Nominal><Name>СДР (специальные права заимствования)</Name><Value>109,7855</Value></Valute><Valute ID="R01625"><NumCode>702</NumCode><CharCode>SGD</CharCode><Nominal>1</Nominal><Name>Сингапурский доллар</Name><Value>59,1645</Value></Valute><Valute ID="R01670"><NumCode>972</NumCode><CharCode>TJS</CharCode><Nominal>10</Nominal><Name>Таджикских сомони</Name><Value>64,0283</Value></Valute><Valute ID="R01700J"><NumCode>949</NumCode><CharCode>TRY</CharCode><Nominal>10</Nominal><Name>Турецких лир</Name><Value>54,7075</Value></Valute><Valute ID="R01710A"><NumCode>934</NumCode><CharCode>TMT</CharCode><Nominal>1</Nominal><Name>Новый туркменский манат</Name><Value>22,8696</Value></Valute><Valute ID="R01717"><NumCode>860</NumCode><CharCode>UZS</CharCode><Nominal>10000</Nominal><Name>Узбекских сумов</Name><Value>70,7100</Value></Valute><Valute ID="R01720"><NumCode>980</NumCode><CharCode>UAH</CharCode><Nominal>10</Nominal><Name>Украинских гривен</Name><Value>27,1570</Value></Valute><Valute ID="R01760"><NumCode>203</NumCode><CharCode>CZK</CharCode><Nominal>10</Nominal><Name>Чешских крон</Name><Value>35,6526</Value></Valute><Valute ID="R01770"><NumCode>752</NumCode><CharCode>SEK</CharCode><Nominal>10</Nominal><Name>Шведских крон</Name><Value>84,7660</Value></Valute><Valute ID="R01775"><NumCode>756</NumCode><CharCode>CHF</CharCode><Nominal>1</Nominal><Name>Швейцарский франк</Name><Value>85,6082</Value></Valute><Valute ID="R01810"><NumCode>710</NumCode><CharCode>ZAR</CharCode><Nominal>10</Nominal><Name>Южноафриканских рэндов</Name><Value>54,6437</Value></Valute><Valute ID="R01815"><NumCode>410</NumCode><CharCode>KRW</CharCode><Nominal>1000</Nominal><Name>Вон Республики Корея</Name><Value>65,0973</Value></Valute><Valute ID="R01820"><NumCode>392</NumCode><CharCode>JPY</CharCode><Nominal>100</Nominal><Name>Японских иен</Name><Value>63,3257</Value></Valute></ValCurs>'
    root = ET.fromstring(tree)
    courses = []
    for child in root:
        courses_currency = child[1].text
        courses_course = child[4].text
        courses_course = courses_course.replace(',', '.', 1)
        courses.append({'rate':courses_course, 'currency': courses_currency})
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
    if request.method == 'GET' and request.GET.get('start-date') and request.GET.get('end-date'):
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


def stats(request):
    if request.user.id is None:
        return redirect('login')
    
    context = {}

    user_currencies = Balances.objects.select_related().filter(user_id=request.user.id).values('currency_id__name')

    context['user_currencies'] = user_currencies

    month = request.GET.get('outlay-month-select') if request.GET.get('outlay-month-select') else datetime.now().month
    outlay_currency = request.GET.get('outlay-currency') if request.GET.get('outlay-currency') else user_currencies[0]['currency_id__name']

    monthly_outlay_data = Operations.objects.select_related().filter(
        user_id=request.user.id,
        operation_type='-'
    ).annotate(
        month=ExtractMonth('datetime'),
        day=ExtractDay('datetime')
    ).values('month', 'day', 'amount').filter(
        month=month,
        currency=outlay_currency
    )

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
                all_amount += float(i.amount) * float(z['rate'])
                break
        else:
            result.append(['RUB', float(i.amount)])
            all_amount += float(i.amount)
    answer = []
    for i in result:
        answer.append([i[0], i[1] / all_amount*100])
    context['exchanged_balances'] = answer
    example_budget_data = []
    if request.GET.get('wallet-start-date') and request.GET.get('wallet-end-date'):
        date_range = [
            request.GET['wallet-start-date'],
            request.GET['wallet-end-date']
        ]
    else:
        date_range = [
            date.today() - timedelta(days=180),
            date.today()
        ]
    if request.GET.get('wallet-currency'):
        wallet_currency = request.GET['wallet-currency']
    else:
        try:
            cur = Balances.objects.select_related().filter(user_id=request.user.id).values('currency_id__name')
            wallet_currency = cur[0]['currency_id__name']
        except:
            wallet_currency = ''
    if request.GET.get('wallet-type') == 'Расходы':
        operation_type = '-'
        context['wallet_type'] = 'Расходы'
    else:
        operation_type = '+'
        context['wallet_type'] = 'Доходы'

    example_income_data = Operations.objects.select_related().filter(
        user_id=request.user.id,
        operation_type=operation_type,
        datetime__range=date_range,
        currency=wallet_currency
    ).values('datetime').annotate(total=Sum('amount'))

    context['income_currency'] = wallet_currency

    if request.GET.get('category-start-date') and request.GET.get('category-end-date'):
        category_daterange = [request.GET['category-start-date'],
                 request.GET['category-end-date']]
    else:
        category_daterange = [date.today() - timedelta(days=180),
                 date.today()]

    if request.GET.get('category-currency'):
        category_currency = request.GET['category-currency']
    else:
        try:
            cat_cur = Balances.objects.select_related().filter(user_id=request.user.id).values('currency_id__name')
            category_currency = cat_cur[0]['currency_id__name']
        except:
            category_currency = ''

    example_category_data = Operations.objects.select_related('category__category_name').filter(
        user_id=request.user.id,
        operation_type='-',
        datetime__range=category_daterange,
        currency=category_currency
    ).values('category__category_name').annotate(total=Sum('amount'))

    context['category_currency'] = category_currency

    if request.GET.get('export-start-date') and request.GET.get('export-end-date'):
        date_range = [
            request.GET.get('export-start-date'),
            request.GET.get('export-end-date')
        ]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.now()) + '.xls'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Операции')
        
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Тип операции', 'Категория', 'Сумма', 'Валюта', 'Дата', 'Описание']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Operations.objects.filter(
            user=request.user.id,
            datetime__range=date_range,
        ).values_list(
            'operation_type', 
            'category_id__category_name', 
            'amount', 
            'currency', 
            'datetime', 
            'description'
        )

        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        
        wb.save(response)
        
        return response

    data_formatted = []
    for elem in example_income_data:
        data_formatted.append([elem['datetime'].strftime("%Y-%m-%d"), float(elem['total'])])

    context['data_income'] = data_formatted


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
