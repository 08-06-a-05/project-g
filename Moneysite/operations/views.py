from django.shortcuts import render
from account_manager.models import *
from operations.models import *

def personal_account(request):
    user_balances = Balances.objects.select_related().filter(user_id=request.user.id)

    print(user_balances)
    context = {
        'balance': user_balances,
    }

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