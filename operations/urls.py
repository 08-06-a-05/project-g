from django.urls import path
from . import views
from . import answer
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('LK/', views.personal_account, name='LK'),
    path('stats/', views.stats, name='LK-stats'),
    path('answer/', answer.ans, name='answer'),
] + staticfiles_urlpatterns()
