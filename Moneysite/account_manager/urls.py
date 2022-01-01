from django.urls import path

from . import views

urlpatterns=[
    path('registration',views.registration_page,name='registration'),
    path('authorization',views.authorization_page,name='authorization'),
    path('', views.main_page ,name='main'),
]
