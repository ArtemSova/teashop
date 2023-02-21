# Generated by Django 4.1.7 on 2023-02-18 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='banner_imgs/', verbose_name='Изображение')),
                ('alt_text', models.CharField(max_length=25, null=True)),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': '1.Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, null=True, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cat_imgs/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': '2.Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True, verbose_name='Название')),
                ('slug', models.CharField(max_length=30, null=True)),
                ('detail', models.TextField(max_length=400, null=True, verbose_name='Описание')),
                ('image', models.ImageField(null=True, upload_to='prod_imgs/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='Цена')),
                ('status', models.BooleanField(default=True, verbose_name='Статутс')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Рекомендованое')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': '3.Товары',
            },
        ),
    ]