from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Вам необходимо указать Email.")
        if not username:
            raise ValueError("Вам необходимо указать пароль.")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_staff = True

        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    displayed_currency = models.CharField(max_length=30,default='ruble')
    balance = models.BigIntegerField(default=0)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    



