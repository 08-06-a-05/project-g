from django.db import models
import datetime

class Users(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    displayed_currency = models.CharField(max_length=30,default='ruble')
    balance = models.BigIntegerField(default=0)


class Categories(models.Model):
    category_name = models.CharField(max_length=30)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Operations(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=datetime.date.today())
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=30,default='ruble')
    description = models.TextField(blank=True)
