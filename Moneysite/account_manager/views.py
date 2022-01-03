from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str

from .forms import CreateUserForm
from .utils import generate_token
from .models import Users



# Create your views here.


def registration_page(request):
    form = CreateUserForm(use_required_attribute=False)
    emails=list(Users.objects.values_list('email',flat=True))
    if request.method == 'POST':
        form = CreateUserForm(request.POST, use_required_attribute=False)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            current_site = get_current_site(request)
            
            email_body = render_to_string('mail_snippets/activate_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email = EmailMessage(
                subject='Активируйте Ваш аккаунт', 
                body=email_body, 
                from_email=settings.EMAIL_HOST_USER,
                to=[form.cleaned_data.get('email')]
            )

            email.send()
            
            messages.add_message(request, messages.SUCCESS,
                                 'Мы отправили Вам письмо для подтверждения регистрации.')
            
            return redirect('login')
    

    return render(request,'registration_page.html', {'form': form,'emails':emails})

def authorization_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.add_message(request, messages.ERROR, 'Обнаружены ошибки в пароле или электронной почте. Проверьте, пожалуйста, правильность введенных данных.')
            return redirect('login')
        elif not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Ваша элеткронная почта не подтверждена. Проверьте, пожалуйста, почтовый ящик.')
            return redirect('login')
        else:
            login(request, user)
            return redirect('main')
    context = {}
    return render(request, 'login.html', context)

def logout_request(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('main')
    

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Ваша почта подтверждена.')
        return redirect('login')
    
    return HttpResponse('failed')

def main_page(request):
    context = {}
    return render(request, 'main.html', context) 