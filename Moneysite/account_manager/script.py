import json
from django.http.response import JsonResponse
from .models import Users
from django.core.validators import validate_email
def valid_email(request):
    email=json.load(request)["email"]
    try: 
        validate_email(email)
    except:
        return JsonResponse({'is_exist':'false','is_registered':'false'})
    else:
        if email in list(Users.objects.values_list("email",flat=True)):
            print(20)
            return JsonResponse({'is_exist':'true','is_registered':'true'})
        else:
            print(40)
            return JsonResponse({'is_exist':'true','is_registered':'false'})