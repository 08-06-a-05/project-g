from django.contrib import admin

# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('email', 'name', 'password')

    readonly_fields = ('balance', 'currency', 'displayed_currency')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()