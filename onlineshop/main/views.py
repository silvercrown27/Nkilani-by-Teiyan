import hashlib
import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import *
from django.shortcuts import render, redirect


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


def landing_page(request):
    media_files = []
    image_extensions = ('.png', '.jpg', '.jfif')
    video_extensions = ('.gif', '.mp4', '.mkv')
    for dirpath, dirname, filenames in os.walk(settings.MEDIA_ROOT):
        for file in filenames:
            if file.endswith(image_extensions + video_extensions):
                path = os.path.join(remove_media_root(dirpath), file)
                ext = file.split(".")[1]
                media_files.append([path, f".{ext}"])

    context = {"media_files": media_files, "v_ext": video_extensions, "i_ext": image_extensions}
    return render(request, "overview.html")


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

        # Check if email already exists in UsersAuth
        if UsersAuth.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'registration_page.html', {'error_message': error_message})

        UsersAuth.objects.create(email=email, password=password_hash)
        Customers.objects.create(first_name=firstname, last_name=lastname, email=email)

        return redirect('signin')

    return render(request, 'Sign in.html')


def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password = hashlib.sha256(password.encode()).hexdigest()
    try:
        user = UsersAuth.objects.get(email=email)
        if password == user.password:
            request.session['user_id'] = f"{user.id}"
            url = reverse('userview:user-home', args=[user.id])
            return redirect(url)
        else:
            return HttpResponse('incorrect Password')
    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the Email {email}")


def wishlist_page(request):
    return render(request, "wishlist-prev.html")
