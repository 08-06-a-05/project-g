from django.db import models
from django.utils import timezone
from account_manager import models as accountModels

class Categories(models.Model):
    category_name = models.CharField(max_length=60)
    user = models.ForeignKey(accountModels.Users, on_delete=models.CASCADE)

class Operations(models.Model):
    user = models.ForeignKey(accountModels.Users, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=1)
    datetime = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    currency = models.CharField(max_length=60, default='RUR')
    description = models.TextField(blank=True)

