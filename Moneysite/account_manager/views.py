from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm

# Create your views here.
def registration_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, form.cleaned_data.get('username') + ', Ваш аккаунт был успешно создан!')

            return redirect('login')

    
    context = {'form': form}
    return render(request,'registration_page.html',context)

def authorization_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            print('nah :(')
    context = {}
    return render(request, 'login.html', context)

def main_page(request):
    return HttpResponse('glavnaia')