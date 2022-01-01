from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views

urlpatterns=[
    path('register/', views.registration_page, name='register'),
    path('login/',views.authorization_page, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.main_page, name='main'),
    
    path('activate_user/<uidb64>/<token>', views.activate_user, name='activate'),
]
