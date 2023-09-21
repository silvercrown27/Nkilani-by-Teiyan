from django.contrib import messages
from django.contrib.sites import requests
from django.http import Http404, JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_daraja.views import stk_push_callback_url
import requests
import base64
from datetime import datetime
from decouple import config

from mpesa.core import MpesaClient

from main.models import Customers
from adminview.models import Product
from .models import *
from .utils import verify_transaction, initialize_transaction


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


@login_required(login_url='/overview/')
def home_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        products = Product.objects.all()[:8]

        context = {"products": products, 'user': user, "customer": customer}
        return render(request, 'userview/index.html', context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def cart_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart) if cart else []

        context = {'user': user, 'cart_items': cart_items, "customer": customer}

        return render(request, "userview/cart.html", context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def contact_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        context = {'user': user, "customer":customer}
        return render(request, "userview/contact.html", context)
    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def checkout_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        context = {'user': user, "customer": customer}

        return render(request, "userview/checkout.html", context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def detail_page(request, prodid):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        product = get_object_or_404(Product, id=prodid)

        reviews = Review.objects.filter(product=product)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        context = {
            'user': user,
            "customer": customer,
            'product': product,
            'reviews': reviews,
            'related_products': related_products,
        }
        return render(request, "userview/detail.html", context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def shop_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        products = Product.objects.all()
        context = {"products": products, 'user': user, "customer": customer}

        return render(request, "userview/shop.html", context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def wishlist_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        wishlist_items = FavoriteProduct.objects.filter(user=customer)
        products = [item.product for item in wishlist_items]

        context = {'user': user, "customer": customer, 'products': products}

        return render(request, "userview/wishlist.html", context)

    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def initiate_payment(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        if request.method == "POST":
            # email = request.POST.get("email")
            # amount = int(request.POST.get("amount")) * 100
            #
            # card_number = request.POST.get("cardNumber")
            # expiration_month = request.POST.get("expirationMonth")
            # expiration_year = request.POST.get("expirationYear")
            # cvc = request.POST.get("cvc")
            #
            # response = initialize_transaction(email, amount, card_number, expiration_month, expiration_year, cvc)
            #
            # authorization_url = response['data']['authorization_url']
            return redirect("userview:c2b-mpesa-transaction")

        return render(request, "userview/checkout.html")

    except Customers.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})


def verify_payment(request):
    if request.method == "GET":
        reference = request.GET.get("reference")
        response = verify_transaction(reference)

        if response['status']:
            transaction_data = response['data']
            print(transaction_data)

    return render(request, "userview/verify_payment.html")


def add_to_wishlist(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            customer = Customers.objects.get(id=user.id)

            existing_wishlist_item = FavoriteProduct.objects.filter(user=customer, product_id=product_id)

            if existing_wishlist_item.exists():
                existing_wishlist_item.delete()
                return JsonResponse({'success': True, 'message': 'Product removed from wishlist'})
            else:
                FavoriteProduct.objects.create(user=customer, product_id=product_id)
                return JsonResponse({'success': True, 'message': 'Product added to wishlist'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Customers.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})


def add_to_cart(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity', 1)
            product = get_object_or_404(Product, id=product_id)
            print("Adding item to cart")

            existing_cart_item = CartItem.objects.filter(cart__customer=customer, product=product)

            if existing_cart_item.exists():
                existing_cart_item = existing_cart_item.first()
                existing_cart_item.quantity += int(quantity)
                existing_cart_item.save()
            else:
                cart, created = Cart.objects.get_or_create(customer=customer)
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Customers.DoesNotExist:
        raise Http404(f"No user registered under the id {user.id}")


def add_review(request, prodid):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)
        print("Product added to cart")

        if request.method == 'POST':
            product = get_object_or_404(Product, id=prodid)

            rating = request.POST.get('rating')
            text = request.POST.get('text')

            review = Review(product=product, user_id=customer.id, rating=rating, text=text)
            review.save()

            messages.success(request, 'Your review has been added successfully.')

            return redirect('userview:prod-detail', prod_name=product.name)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except Customers.DoesNotExist:
        raise Http404(f"No user registered under the id {user.id}")


def oath_success():
    cl = MpesaClient()
    r = cl.access_token()
    print(r)
    stk_push_success(cl)
    return JsonResponse(r, safe=False)


def stk_push_success(cl):
    number = config('LNM_PHONE_NUMBER')
    amount = 1
    account_ref = 'ABC001'
    transaction_desc = 'STK Push Description'
    callback_url = stk_push_callback_url
    response = cl.stk_push(number, amount, account_ref, transaction_desc, callback_url)
    return JsonResponse(response, safe=False)


def lipa_na_mpesa_online(request):
    cl = MpesaClient()
    access_token = cl.access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    BusinessShortCode = config('MPESA_EXPRESS_SHORTCODE')

    # Generate the password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = config('MPESA_PASSKEY')
    password = base64.b64encode((BusinessShortCode + passkey + timestamp).encode('ascii')).decode('utf-8')

    PartyA = "254743687737"
    PartyB = BusinessShortCode
    PhoneNumber = "254743687737"
    AccountReference = "Bradley"
    TransactionDesc = "Testing stk push"

    request_data = {
        "BusinessShortCode": BusinessShortCode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": 1,
        "PartyA": PartyA,
        "PartyB": PartyB,
        "PhoneNumber": PhoneNumber,
        "CallBackURL": stk_push_callback_url,
        "AccountReference": AccountReference,
        "TransactionDesc": TransactionDesc
    }

    resp = requests.post(api_url, json=request_data, headers=headers)
    print(resp)
    return HttpResponse('success')
