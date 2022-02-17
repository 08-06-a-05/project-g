from django.shortcuts import render, redirect
from django.db.models import Sum
from account_manager.models import *
from operations.models import *
from operations.forms import AddOperationForm
from django.db.models.functions import TruncDay
from datetime import date
from datetime import timedelta
from json import dumps
from .currency_exchange_rate_parsing.parsing import CurrencyConverter
import itertools


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
        user_operations = Operations.objects.select_related().filter(user_id=request.user.id,
                                                                     datetime__range=[request.GET['start-date'],
                                                                                      request.GET[
                                                                                          'end-date']]).order_by(
            '-datetime')
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

    example_outlay_data = Operations.objects.select_related().filter(user_id=request.user.id, operation_type='-',
                                                                     datetime__range=[date.today() - timedelta(days=10),
                                                                                      date.today()]).values('datetime').annotate(total=Sum('amount'))

    example_budget_data = []
    if 'start-date' in request.GET:
        example_income_data = Operations.objects.select_related().filter(user_id=request.user.id, operation_type='+',
                                                                         datetime__range=[
                                                                             request.GET['start-date'],
                                                                             request.GET['end-date']]).values('datetime').annotate(total=Sum('amount'))
    else:
        example_income_data = Operations.objects.select_related().filter(user_id=request.user.id, operation_type='+',
                                                                     datetime__range=[date.today() - timedelta(days=10),
                                                                                      date.today()]).values('datetime').annotate(total=Sum('amount'))

    example_category_data= Operations.objects.select_related('category__category_name').filter(user_id=request.user.id, operation_type='-',
                                                                     datetime__range=[date.today() - timedelta(days=10),
                                                                                      date.today()]).values('category__category_name').annotate(total=Sum('amount'))
    print(request.GET)
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

    context['data_budget'] = example_budget_data

    return render(request, 'LK_stats.html', context)
