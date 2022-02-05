from django.shortcuts import render


# Create your views here.

def personal_account(request):
    context = {}
    return render(request, 'manager.html', context)

def example(request):
    context = {}
    return render(request, 'LK.html', context)
