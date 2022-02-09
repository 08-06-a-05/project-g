from django.contrib import admin
from account_manager.models import Users, Balances, Currency 

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'displayed_currency', 'is_email_verified')

@admin.register(Balances)
class BalancesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'currency_id', 'amount')
    
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'name')