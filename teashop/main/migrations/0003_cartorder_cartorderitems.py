# Generated by Django 4.1.7 on 2023-02-19 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_remove_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.FloatField(verbose_name='Итого')),
                ('paid_status', models.BooleanField(default=False, verbose_name='Статус платежа')),
                ('order_dt', models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': '8. Заказы',
            },
        ),
        migrations.CreateModel(
            name='CartOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=150, verbose_name='Счет-фактура')),
                ('item', models.CharField(max_length=150, verbose_name='Товар')),
                ('image', models.CharField(max_length=200, verbose_name='Изображение')),
                ('qty', models.IntegerField(verbose_name='Количество')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('total', models.FloatField(verbose_name='Итого')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cartorder', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Товары заказа',
                'verbose_name_plural': '9. Товары заказа',
            },
        ),
    ]
