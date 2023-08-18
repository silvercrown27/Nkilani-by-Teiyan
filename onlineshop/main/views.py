from django.shortcuts import render


# Create your views here.
def landing_page(requests):
    return render(requests, "index.html")


def cart_page(requests):
    return render(requests, "cart.html")


def contact_page(requests):
    return render(requests, "contact.html")


def checkout_page(requests):
    return render(requests, "checkout.html")


def detail_page(requests):
    return render(requests, "detail.html")


def shop_page(requests):
    return render(requests, "shop.html")


def signin_page(requests):
    return render(requests, "Sign in.html")


def signup_page(requests):
    return render(requests, "Sign Up.html")


def wishlist_page(requests):
    return render(requests, "wishlist.html")
