# Generated by Django 4.1.7 on 2023-02-23 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_cartorder_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('process', 'Обрабатывается'), ('shipped', 'Доставляется'), ('delivered', 'Доставлено')], default='process', max_length=150, verbose_name='Статус заказа'),
        ),
    ]
