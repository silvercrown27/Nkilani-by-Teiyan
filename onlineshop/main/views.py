import hashlib

from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import *
from django.shortcuts import render, redirect
from .utils import initialize_transaction, verify_transaction


def landing_page(request):
    return render(request, "index.html")


def cart_page(request):
    return render(request, "cart.html")


def contact_page(request):
    return render(request, "contact.html")


def checkout_page(request):
    return render(request, "checkout.html")


def detail_page(request):
    return render(request, "detail.html")


def shop_page(request):
    return render(request, "shop.html")


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

        # Check if email already exists in UsersAuth
        if UsersAuth.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'registration_page.html', {'error_message': error_message})

        UsersAuth.objects.create(email=email, password=password_hash)
        Customers.objects.create(first_name=firstname, last_name=lastname, email=email)

        return redirect('/signin/')

    return render(request, 'Sign in.html')


def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password = hashlib.sha256(password.encode()).hexdigest()
    try:
        user = UsersAuth.objects.get(email=email)
        if password == user.password:
            request.session['user_id'] = user.id
            url = reverse('userview:home', args=[user.id])
            return redirect(url)
        else:
            return HttpResponse('incorrect Password')
    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the Email {email}")


def wishlist_page(request):
    return render(request, "wishlist.html")


def checkout():
    pass


def initiate_payment(request):
    if request.method == "POST":
        email = request.POST.get("email")
        amount = int(request.POST.get("amount")) * 100

        card_number = request.POST.get("cardNumber")
        expiration_month = request.POST.get("expirationMonth")
        expiration_year = request.POST.get("expirationYear")
        cvc = request.POST.get("cvc")

        response = initialize_transaction(email, amount, card_number, expiration_month, expiration_year, cvc)

        authorization_url = response['data']['authorization_url']
        return redirect(authorization_url)

    return render(request, "checkout.html")


def verify_payment(request):
    if request.method == "GET":
        reference = request.GET.get("reference")
        response = verify_transaction(reference)

        if response['status']:
            transaction_data = response['data']
            print(transaction_data)

    return render(request, "verify_payment.html")
