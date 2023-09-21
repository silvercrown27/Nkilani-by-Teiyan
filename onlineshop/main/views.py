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
    product = get_object_or_404(Product, pk=product_id)

    user_session = request.session.session_key
    cart_item, created = UserCartItem.objects.get_or_create(
        user_session=user_session,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/detail/', product_id=product.id)


def landing_page(request):
    products = Product.objects.all()
    # for product in products:
    #     print(f"Product Name: {product.name}")
    #     print(f"Product Description: {product.description}")
    #     print(f"Product Category: {product.category}")
    #     print(f"Product Price: {product.price}")
    #     print(f"Product Image: {product.image}")
    #     print("-" * 30)

    context = {"products": products}
    return render(request, "main/overview.html", context)


def cart_page(request):
    return render(request, "main/cart-prev.html")


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


def wishlist_page(request):
    return render(request, "wishlist-prev.html")


def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("newsletter_email")
        print("<" + "-"*20 + "email:" + email)

        Newsletter.objects.create(email=email).save()
    return redirect("/")
