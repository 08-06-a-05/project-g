from django.db import migrations
from operations.views import get_courses

def append_currencies(apps, schema_editor):
    currencies = get_courses()

    Currency = apps.get_model('account_manager', 'Currency')
    for rate in currencies:
        Currency.objects.create(name=rate['currency'])


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0004_alter_currency_name'),
    ]

    operations = [
        migrations.RunPython(append_currencies)
    ]
