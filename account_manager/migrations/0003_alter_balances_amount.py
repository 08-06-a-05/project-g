# Generated by Django 4.0 on 2022-02-12 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0002_alter_balances_amount_alter_users_displayed_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balances',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100, null=True),
        ),
    ]
