from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
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


def verify_payment(request):
    reference = request.POST.get('reference')  # Get the reference from the AJAX request
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {'Authorization': 'Bearer SECRET_KEY'}

    response = requests.get(url, headers=headers)
    data = response.json()

    # Check the transaction status and take appropriate action
    if data['status']:
        # Transaction is successful, deliver value to customer
        return HttpResponse('Payment successful')
    else:
        # Transaction failed or is pending, handle accordingly
        return HttpResponse('Payment not successful')
