from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    displayed_currency = models.CharField(max_length=30)
    balance = models.BigIntegerField()


class Categories(models.Model):
    category_name = models.CharField(max_length=30)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Operations(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=30)
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=30)
    description = models.TextField(blank=True)
