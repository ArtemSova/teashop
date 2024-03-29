# Generated by Django 4.1.7 on 2023-02-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_cartorder_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('Обрабатывается', 'Обрабатывается'), ('Доставляется', 'Доставляется'), ('Доставлено', 'Выполнен')], default='Обрабатывается', max_length=150, verbose_name='Статус заказа'),
        ),
    ]
