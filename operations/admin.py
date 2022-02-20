from django.contrib import admin
from operations.models import Categories, Operations

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'user')

@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'operation_type', 'amount', 'user')

