from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    displayed_currency = models.CharField(max_length=30,default='ruble')
    balance = models.BigIntegerField(default=0)


