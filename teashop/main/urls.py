from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('category-list', views.category_list, name='category-list'),
    path('product-list', views.product_list, name='product-list'),
    path('category-product-list/<int:cat_id>', views.category_product_list, name='category-product-list'),
    path('product/<int:id>', views.product_detail, name='product-detail'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('load-more-data', views.load_more_data, name='load_more_data'),
    path('load-more-dataCat', views.load_more_dataCat, name='load_more_dataCat'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart_list, name='cart'),
    path('delete-from-cart', views.delete_cart_item, name='delete-from-cart'),
    path('update-cart', views.update_cart_item, name='update-cart'),
    path('accounts/signup', views.signup, name='signup'),
    path('checkout', views.checkout, name='checkout'),
    path('save-review/<int:pid>', views.save_review, name='save_review'),
    # Оплата
    #path('payment/', include('#')),   --------------------------------------------------------- Прикрутить оплату
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    # Личный кабинет
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    path('my-reviews',views.my_reviews, name='my-reviews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)