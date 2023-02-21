from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User


class Banner(models.Model):
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = '1.Баннеры'
    image = models.ImageField(upload_to="banner_imgs/", null=True, blank=True, verbose_name='Изображение')
    alt_text = models.CharField(max_length=25, null=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))

    def __str__(self):
        return self.alt_text

class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '2.Категории'
    title = models.CharField(max_length=25, null=True, verbose_name='Название')
    image = models.ImageField(upload_to="cat_imgs/", null=True, blank=True, verbose_name='Изображение')

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '3.Товары'
    title = models.CharField(max_length=30, null=True, verbose_name='Название')
    # slug = models.CharField(max_length=30, null=True)
    detail = models.TextField(max_length=400, null=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False, verbose_name='Категория')
    image = models.ImageField(upload_to="prod_imgs/", null=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, verbose_name='Цена')
    status = models.BooleanField(default=True, verbose_name='Статутс')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендованое')

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    total_amt = models.FloatField(verbose_name='Итого')
    paid_status = models.BooleanField(default=False, verbose_name='Статус платежа')
    order_dt = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    # order_status = models.CharField(choices=status_choice, default='process', max_length=150, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = '4. Заказы'

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, verbose_name='Заказ')
    invoice_no = models.CharField(max_length=150, verbose_name='Счет-фактура')
    item = models.CharField(max_length=150, verbose_name='Товар')
    image = models.CharField(max_length=200, verbose_name='Количество')
    qty = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    total = models.FloatField(verbose_name='Итого')

    class Meta:
        verbose_name = 'Товары заказа'
        verbose_name_plural = '5. Товары заказа'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    review_text = models.TextField(verbose_name='Отзыв')
    review_rating = models.CharField(choices=RATING, max_length=150, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Рейтинг товара'
        verbose_name_plural = '6. Рейтинги товаров'

    def get_review_rating(self):
        return self.review_text