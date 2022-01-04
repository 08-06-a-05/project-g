import json

from django.http.response import JsonResponse
from .models import Users
def what(request):
    mail=json.load(request)["email"]
    if mail in list(Users.objects.values_list("email",flat=True)):
        print(20)
        return JsonResponse({'is_registered':'true'})
    else:
        print(40)
        return JsonResponse({'is_registered':'false'})