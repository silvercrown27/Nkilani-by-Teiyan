from django.db import models

from main.models import Customers


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class OfferedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateField()
    duration = models.PositiveIntegerField()
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.product.name

