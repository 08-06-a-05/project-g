import json
from django.http.response import JsonResponse


def ans(request):
    email = json.load(request)["email"]
    try:
        validate_email(email)
    except:
        return JsonResponse({'is_exist': 'false', 'is_registered': 'false'})
    else:
        if email in list(Users.objects.values_list("email", flat=True)):
            return JsonResponse({'is_exist': 'true', 'is_registered': 'true'})
        else:
            return JsonResponse({'is_exist': 'true', 'is_registered': 'false'})
