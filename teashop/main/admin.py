from django.contrib import admin
from .models import *


class BannerAdmin(admin.ModelAdmin):
	list_display = ('alt_text', 'image_tag')
admin.site.register(Banner, BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'image_tag', 'status', 'is_featured')
    list_editable = ('status', 'is_featured')
admin.site.register(Product, ProductAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amt', 'paid_status', 'order_status', 'order_dt')
    list_editable = ('paid_status', 'order_status')
admin.site.register(CartOrder, CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'item', 'image_tag', 'qty', 'price', 'total')
admin.site.register(CartOrderItems, CartOrderItemsAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review_text', 'get_review_rating')
admin.site.register(ProductReview, ProductReviewAdmin)

admin.site.register(Wishlist)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display=('user', 'address', 'status')
admin.site.register(UserAddressBook, UserAddressBookAdmin)