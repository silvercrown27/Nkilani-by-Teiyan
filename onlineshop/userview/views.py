from django.http import Http404
from django.conf import settings
from django.shortcuts import render, redirect

from main.models import UsersAuth
from adminview.models import Product
from .models import *
from .utils import verify_transaction, initialize_transaction


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


def home_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        products = Product.objects.all()[:8]
        context = {"products": products, 'user': user}

        return render(request, 'index.html', context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def cart_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, "cart.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def contact_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, "contact.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def checkout_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, "checkout.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def detail_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, "detail.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def shop_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        products = Product.objects.all()
        context = {"products": products, 'user': user}

        return render(request, "shop.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def wishlist_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, "wishlist.html", context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def initiate_payment(request, userid):
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


def verify_payment(request, userid):
    if request.method == "GET":
        reference = request.GET.get("reference")
        response = verify_transaction(reference)

        if response['status']:
            transaction_data = response['data']
            print(transaction_data)

    return render(request, "verify_payment.html")


def add_to_wishlist(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, 'index.html', context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")


def add_to_cart(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != f"{user.id}":
            return redirect('/signin/')

        context = {'user': user}

        return render(request, 'index.html', context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")
    