import os
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import Product

from main.models import UsersAuth


from PIL import Image
import os


class ImageResizer:
    def __init__(self, image_path):
        self.image = image_path
        self.iterate_items(self.image)

    def resize_image(self, input_path, output_path, new_width, new_height):
        try:
            with Image.open(input_path) as img:
                img.thumbnail((new_width, new_height))
                default_path = "My Products"
                fs = FileSystemStorage()
                file_path = os.path.join(settings.MEDIA_ROOT, default_path)
                output_file_path = os.path.join(file_path, output_path)

                fs.save(output_file_path, img)
                print(f"Image resized and saved as {output_file_path}")

        except IOError:
            print("Unable to resize image.")

    def is_image(self, file_path):
        try:
            with Image.open(file_path) as img:
                return True
        except (OSError, Image.UnidentifiedImageError):
            return False

    def iterate_items(self, path):
        try:
            output_dir = os.path.join(path, self.image)
            os.makedirs(output_dir, exist_ok=True)

            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    if self.is_image(item_path):
                        output_path = os.path.join(output_dir, item)
                        self.resize_image(item_path, output_path, 840, 1280)
                    else:
                        print(f"Found non-image file: {item_path}")

        except OSError as e:
            print(f"Error: {e}")


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
            return render(request, 'admin section.html', {'error_message': error_message})

        default_path = "My Products"
        fs = FileSystemStorage()
        file_path = os.path.join(settings.MEDIA_ROOT, default_path, image.name)
        fs.save(file_path, image)
        ImageResizer(file_path)

        Product.objects.create(name=name, description=description, image=os.path.join(default_path, image.name),
                               price=price, category=category)

    return render(request, 'admin section.html')
