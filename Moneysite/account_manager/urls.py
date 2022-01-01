from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views

urlpatterns=[
    path('register/', views.registration_page, name='register'),
    path('login/',views.authorization_page, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.main_page, name='main'),

    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name="password_reset/password_reset.html"
        ), 
        name="password_reset",
    ),

    path('password_reset_sent/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/password_reset_sent.html"
        ), 
        name="password_reset_done",
    ),

    path('password_reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/password_reset_page.html'
        ), 
        name="password_reset_confirm"
        ),
    path(
        'password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_done.html"
        ), 
        name="password_reset_complete",
    ),
    
    path('activate_user/<uidb64>/<token>', views.activate_user, name='activate'),
]
