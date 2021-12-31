# Generated by Django 4.0 on 2021-12-30 20:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=60)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_manager.users')),
            ],
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(max_length=30)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.PositiveBigIntegerField()),
                ('currency', models.CharField(default='ruble', max_length=60)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operations.categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_manager.users')),
            ],
        ),
    ]
