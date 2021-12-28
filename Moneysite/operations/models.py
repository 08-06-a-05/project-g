from django.db import models
from django.utils import timezone
from account_manager import models as accountModels

class Categories(models.Model):
    category_name = models.CharField(max_length=60)
    user = models.ForeignKey(accountModels.Users, on_delete=models.CASCADE)


class Operations(models.Model):
    user = models.ForeignKey(accountModels.Users, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=60, default='ruble')
    description = models.TextField(blank=True)

