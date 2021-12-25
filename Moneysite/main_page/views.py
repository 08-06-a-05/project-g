from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def registration_page(request):
    return HttpResponse('Hello, world!')

def authorization_page(request):
    return HttpResponse('number 2')

def main_page(request):
    return HttpResponse('glavnaia')