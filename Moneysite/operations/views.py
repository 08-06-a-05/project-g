from django.shortcuts import render


# Create your views here.

def personal_account(request):
    context = {}
    return render(request, 'manager.html', context)

def example(request):
    context = {}
    return render(request, 'LK.html', context)


def example_stat(request):
    context = {}
    return render(request, 'LK_statistics.html', context)
