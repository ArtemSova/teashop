from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Max, Min, Count, Avg
from django.template.loader import render_to_string
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#Payment
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured=True).order_by('-id')
    return render(request, 'index.html', {'data': data, 'banners': banners})

def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'category_list.html', {'data': data})

def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:1]
    cats = Product.objects.distinct().values('category__title', 'category__id')
    return render(request, 'product_list.html',
                  {
                      'data': data,
                      'cats': cats,
                      'total_data': total_data,
                  })

def category_product_list(request, cat_id):
    category = Category.objects.get(id=cat_id)
    total_data = Product.objects.filter(category=category).count()
    data = Product.objects.filter(category=category).order_by('-id')[:1]
    return render(request, 'category_product_list.html', {'data': data, 'total_data': total_data, 'category': category})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    reviewForm = ReviewAdd()

    # Проверка
    canAdd = True
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
        if reviewCheck > 0:
            canAdd = False
    # Проверка End

    # Запрос отзывов
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Запрос рейтинга
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'product_detail.html', {'data': product, 'related': related_products, 'form': reviewForm, 'canAdd': canAdd, 'reviews': reviews, 'avg_reviews': avg_reviews})

def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__iregex=q).order_by('-id')
    # data = Product.objects.filter(title__icontains=q).order_by('-id') латиница
    return render(request, 'search.html', {'data': data})

def filter_data(request):
    categories = request.GET.getlist('category[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(price__gte=minPrice)
    allProducts = allProducts.filter(price__lte=maxPrice)
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})

def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t}
)

def load_more_dataCat(request):
    category = Category.objects.all()
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.filter(category__id__in=category).order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/category_product_list.html', {'data': data})
    return JsonResponse({'data': t})

def add_to_cart(request):
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'qty': request.GET['qty'],
        'title': request.GET['title'],
        'image': request.GET['image'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

def cart_list(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})

def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})

# Checkout
@login_required
def checkout(request):
    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*float(item['price'])
        # Order
        order = CartOrder.objects.create(
                user=request.user,
                total_amt=totalAmt
            )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
                )
            # End
        # Process Payment
        host = request.get_host()
        payment_dict = {
            # 'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-'+str(order.id),
            'invoice': 'INV-'+str(order.id),
            'currency_code': 'RUB',
        }
        # form = PaymentForm(initial=payment_dict)
        # address = UserAddressBook.objects.filter(user=request.user, status=True).first()
        return render(request, 'checkout.html',{'cart_data':request.session['cartdata'], 'totalitems':len(request.session['cartdata']),'total_amt':total_amt}) # 'form':form,'address':address

@csrf_exempt
def payment_done(request):
    returnData=request.POST
    return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')


def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating'],
    }

    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})

# Профиль
def my_dashboard(request):
    return render(request, 'user/dashboard.html')

def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})

def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html',{'orderitems':orderitems})

def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product, user=request.user).count()
    if checkw > 0:
        data={
            'bool':False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool':True
        }
    return JsonResponse(data)

def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wlist': wlist})

def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews':reviews})

