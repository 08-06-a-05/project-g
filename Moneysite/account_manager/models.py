from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUsersManager(BaseUserManager):
    def create_user(self, email, username, password):
        user = self.model(email=email, username=username, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    displayed_currency = models.CharField(max_length=30, default='RUB')
    
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = CustomUsersManager()

    def __str__(self):
        return self.email

    def natural_key(self):
        return self.email

    def get_short_name(self):
        return self.email

class Currency(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Balances(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)


