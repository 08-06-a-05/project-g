from django.urls import path
from . import views

urlpatterns = [
    path('LK/', views.personal_account, name='LK'),
]
