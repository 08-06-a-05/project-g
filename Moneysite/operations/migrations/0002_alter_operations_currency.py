# Generated by Django 4.0 on 2022-02-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operations',
            name='currency',
            field=models.CharField(default='RUB', max_length=60),
        ),
    ]
