from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('contact/', views.cart_page, name="contact"),
    path('wishlist/', views.wishlist_page, name="wishlist"),
    path('detail/', views.detail_page, name="detail"),
    path('cart/', views.cart_page, name="cart"),
    path('shop/', views.shop_page, name="shop"),
    path('signin/', views.signin_page, name="signin"),
    path('signup/', views.signup_page, name="signup"),
    path('checkout/', views.checkout_page, name="checkout"),
]
