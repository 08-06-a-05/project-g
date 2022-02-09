from django.shortcuts import render
from account_manager.models import *
from operations.models import *

def personal_account(request):
    user_balances = list(
        Balances.objects.select_related().filter(user_id=request.user.id)[:3]
    )
    
    context = {
        # 'currency1': str(user_balances[0].currency_id),
        # 'currency2': str(user_balances[1].currency_id),
        # 'currency3': str(user_balances[2].currency_id),
        # 'amount1': user_balances[0].amount,
        # 'amount2': user_balances[1].amount,
        # 'amount3': user_balances[2].amount,
    }

    return render(request, 'manager.html', context)

def example(request):
    context = {}
    return render(request, 'LK.html', context)


def example_stat(request):
    context = {}
    return render(request, 'LK_statistics.html', context)
