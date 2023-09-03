from django.db import models

from main.models import Customers
from adminview.models import Product


class Cart(models.Model):
    customer = models.OneToOneField(Customers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.customer.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart for {self.cart.customer.name}"


class FavoriteProduct(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    timestamp = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    paystack_response = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.name} for {self.product.name}"
