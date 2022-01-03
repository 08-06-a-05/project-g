import json

from django.http.response import JsonResponse
from .models import Users
def what(request):
    mail=json.load(request)["email"]
    if mail in list(Users.objects.values_list("email",flat=True)):
        return JsonResponse({'field':'yes'})
    else:
        return JsonResponse({'field':'no'})