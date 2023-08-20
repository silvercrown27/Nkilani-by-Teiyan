import requests
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