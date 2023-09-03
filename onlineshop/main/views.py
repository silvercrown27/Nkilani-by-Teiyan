import hashlib
import os

from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import UsersAuth, AdminAccounts, Customers
from adminview.models import Product
from django.shortcuts import render, redirect


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


def landing_page(request):
    products = Product.objects.all()
    for product in products:
        print(f"Product Name: {product.name}")
        print(f"Product Description: {product.description}")
        print(f"Product Category: {product.category}")
        print(f"Product Price: {product.price}")
        print(f"Product Image: {product.image}")
        print("-" * 30)

    context = {"products": products}
    return render(request, "overview.html", context)



def cart_page(request):
    return render(request, "cart-prev.html")


def contact_page(request):
    return render(request, "contact-prev.html")


def checkout_page(request):
    return render(request, "checkout-prev.html")


def detail_page(request):
    return render(request, "detail-prev.html")


def shop_page(request):
    return render(request, "shop-prev.html")


def signin_page(request):
    return render(request, "Sign in.html")


def signup_page(request):
    return render(request, "Sign Up.html")


def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if UsersAuth.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'registration_page.html', {'error_message': error_message})

        try:
            user_auth = UsersAuth.objects.create(email=email, password=password_hash)
            Customers.objects.create(user=user_auth, first_name=firstname, last_name=lastname)
            return redirect('/signin')
        except IntegrityError:
            error_message = "An error occurred during registration. Please try again."
            return render(request, 'registration_page.html', {'error_message': error_message})

    return render(request, 'Sign in.html')


def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        user = UsersAuth.objects.get(email=email)
        if password_hash == user.password:
            request.session['user_id'] = f"{user.id}"
            try:
                admin_user = AdminAccounts.objects.get(email=email)
                admin_url = reverse('adminview:admin-home', args=[user.id])
                return redirect(admin_url)
            except AdminAccounts.DoesNotExist:
                customer_url = reverse('userview:user-home', args=[user.id])
                return redirect(customer_url)

        else:
            return HttpResponse('Incorrect Password')
    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the Email {email}")


def wishlist_page(request):
    return render(request, "wishlist-prev.html")
