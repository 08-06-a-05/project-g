from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views
from . import script
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('register/', views.registration_page, name='register'),
    path('login/',views.authorization_page, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.main_page, name='main'),
    path('abra/',script.valid_email,name='what'),
    
    path('activate_user/<uidb64>/<token>', views.activate_user, name='activate'),

    path('', include('operations.urls')),
] + staticfiles_urlpatterns()
