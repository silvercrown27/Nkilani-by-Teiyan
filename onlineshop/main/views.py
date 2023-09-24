import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings

from .models import *
from django.contrib.auth.models import User
from adminview.models import Product


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


def add_to_cart(request, product_id):
    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Initialize an empty cart list from cookies or create one if it doesn't exist
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)

    # Add the product to the cart or update the quantity if it already exists
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    # Update the cart in cookies
    response = JsonResponse({'success': True, 'message': 'Product added to cart'})
    response.set_cookie('cart', json.dumps(cart))
    return response


def add_to_wishlist(request, product_id):
    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Initialize an empty wishlist list from cookies or create one if it doesn't exist
    wishlist = request.COOKIES.get('wishlist', '{}')
    wishlist = json.loads(wishlist)

    # Add the product to the wishlist
    wishlist[str(product_id)] = product.name

    # Update the wishlist in cookies
    response = JsonResponse({'success': True, 'message': 'Product added to wishlist'})
    response.set_cookie('wishlist', json.dumps(wishlist))
    return response


def landing_page(request):
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "main/overview.html", context)


def cart_view(request):
    # Initialize an empty cart list from cookies or create one if it doesn't exist
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)

    # Retrieve product details for items in the cart
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})

    return render(request, "main/cart-prev.html", {'cart_items': cart_items, 'total_price': total_price})


def wishlist_page(request):
    # Initialize an empty wishlist list from cookies or create one if it doesn't exist
    wishlist = request.COOKIES.get('wishlist', '{}')
    wishlist = json.loads(wishlist)

    # Retrieve product details for items in the wishlist
    wishlist_items = []
    for product_id, product_name in wishlist.items():
        product = get_object_or_404(Product, id=product_id)
        wishlist_items.append({'product': product, 'product_name': product_name})

    return render(request, "main/wishlist-prev.html", {'wishlist_items': wishlist_items})


def contact_page(request):
    return render(request, "main/contact-prev.html")


def checkout_page(request):
    return render(request, "main/checkout-prev.html")


def detail_page(request):
    return render(request, "main/detail-prev.html")


def shop_page(request):
    products = Product.objects.all()
    context = {"products": products}

    return render(request, "main/shop-prev.html", context)


def signin_page(request):
    return render(request, "main/Sign in.html")


def signup_page(request):
    return render(request, "main/Sign Up.html")


def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'Sign In.html', {'error_message': error_message})

        try:
            print("signing in user")
            user = User.objects.create_user(username=email, email=email, password=password)
            customer = Customers.objects.create(user=user, first_name=firstname, last_name=lastname)
            print(user.id)
            customer.save()

            signin_url = reverse('overview:signin')
            return redirect(signin_url)
        except IntegrityError:
            error_message = "An error occurred during registration. Please try again."
            return render(request, 'main/sign up.html', {'error_message': error_message})

    return render(request, 'main/Sign up.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin_user = AdminAccounts.objects.get(email=email)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                admin_url = reverse('adminview:admin-home', args=[user.username])
                return redirect(admin_url)
            else:
                return JsonResponse({'error': 'Incorrect Email or Password'}, status=400)
        except AdminAccounts.DoesNotExist:
            try:
                user = authenticate(request, username=email, password=password)
                customer = Customers.objects.get(user=user)
                if user is not None:
                    auth_login(request, user)
                    customer_url = reverse('userview:user-home')
                    return redirect(customer_url)
                else:
                    return JsonResponse({'error': 'Incorrect Email or Password'}, status=400)
            except Customers.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

    return render(request, 'main/Sign in.html')


def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("newsletter_email")
        print("<" + "-"*20 + "email:" + email)

        Newsletter.objects.create(email=email).save()
    return redirect("/")
