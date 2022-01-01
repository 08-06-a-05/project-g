from django.urls import path

from . import views

urlpatterns=[
    path('register/', views.registration_page, name='register'),
    path('login/',views.authorization_page, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.main_page, name='main'),
]
