import requests
import base64
from datetime import datetime
from decouple import config

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.sites import requests
from django.http import Http404, JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_daraja.views import stk_push_callback_url

from mpesa.core import MpesaClient
from main.models import Customers, ContactUs
from adminview.models import Product, ProductImage
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
        products = Product.objects.all()

        default_product_image = product.productimage_set.first()
        product_images = ProductImage.objects.filter(product=product)

        reviews = Review.objects.filter(product=product)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        context = {
            'user': user,
            "customer": customer,
            'product': product,
            'products': products,
            'reviews': reviews,
            'related_products': related_products,
            'default_product_image': default_product_image,
            'product_images': product_images,
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


def initiate_payment(request, total_price):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = Customers.objects.get(user=user)

        if request.method == "POST":
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('number')

            response = lipa_na_mpesa_online(phone, total_price)
            return response

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
        print("Wishlist item start")
        customer = Customers.objects.get(user=user)

        if request.method == 'POST':
            print("Wishlist item start")
            product_id = request.POST.get('product_id')

            existing_wishlist_item = FavoriteProduct.objects.filter(user=customer, product_id=product_id)
            print("Item aded to Wishlist")
            if existing_wishlist_item.exists():
                existing_wishlist_item.delete()
                return JsonResponse({'success': True, 'message': 'Product removed from wishlist'})
            else:
                FavoriteProduct.objects.create(user=customer, product_id=product_id)
                return JsonResponse({'success': True, 'message': 'Product added to wishlist'})
        else:
            print("failed to add wish...")
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


def lipa_na_mpesa_online(number, total_amount):
    cl = MpesaClient()
    access_token = cl.access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    BusinessShortCode = config('MPESA_EXPRESS_SHORTCODE')

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = config('MPESA_PASSKEY')
    password = base64.b64encode((BusinessShortCode + passkey + timestamp).encode('ascii')).decode('utf-8')

    PartyA = str(number)[1:]
    print(number)
    print(PartyA)
    PartyB = BusinessShortCode
    PhoneNumber = PartyA
    AccountReference = "Bradley"
    TransactionDesc = "Testing stk push"

    request_data = {
        "BusinessShortCode": BusinessShortCode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": total_amount,
        "PartyA": PartyA,
        "PartyB": PartyB,
        "PhoneNumber": PhoneNumber,
        "CallBackURL": stk_push_callback_url,
        "AccountReference": AccountReference,
        "TransactionDesc": TransactionDesc
    }

    resp = requests.post(api_url, json=request_data, headers=headers)
    print(resp)
    return HttpResponse(resp)


def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactUs.objects.create(name=name, email=email, subject=subject, message=message).save()
        print(f"message from {name} has been sent!")

    return redirect("userview:contact")


def logout_user(request):
    try:
        logout(request)
        return redirect('main:landing_page')
    except:
        return redirect('main:landing_page')
