from .models import Product
from django.db.models import Min, Max
from django.db.models import FloatField


def get_filters(request):
    cats = Product.objects.distinct().values('category__title', 'category__id')
    minMaxPrice = Product.objects.aggregate(Min('price', output_field=FloatField()), Max('price', output_field=FloatField()))
    data = {
        'cats': cats,
        'minMaxPrice': minMaxPrice,
    }
    return data