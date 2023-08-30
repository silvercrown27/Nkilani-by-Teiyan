import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from main.models import Product

from main.models import UsersAuth


def admin_page(request, admin_id):
    return render(request, "admin section.html")


def add_product(request, admin_id):
    if request.method == "POST":
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.FILES.get('product_image')
        price = request.POST.get('product_price')
        category = request.POST.get('product_category')

        if Product.objects.filter(name=name).exists():
            error_message = "Product with this name already exists. Please use a different name."
            return render(request, 'admin_section.html', {'error_message': error_message})

        default_path = "My Products"
        fs = FileSystemStorage()
        file_path = os.path.join(settings.MEDIA_ROOT, default_path, image.name)
        fs.save(file_path, image)

        Product.objects.create(name=name, description=description, image=os.path.join(default_path, image.name),
                               price=price, category=category)

    return render(request, 'admin section.html')