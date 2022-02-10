from django.urls import path
from . import views

urlpatterns = [
    path('LK/', views.personal_account, name='LK'),
    path('example/', views.example, name='LK2'),
    path('examplestat/', views.example_stat, name='LK-statistics'),
    path('stats/', views.stats, name='LK-stats')
]
