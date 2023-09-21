from django.urls import path
from . import views

app_name = "overview"

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('contact', views.contact_page, name="info"),
    path('wishlist', views.wishlist_page, name="wishlist-prev"),
    path('detail', views.detail_page, name="detail-prev"),
    path('cart', views.cart_page, name="cart-prev"),
    path('shop', views.shop_page, name="shop-prev"),
    path('signin', views.signin_page, name="signin"),
    path('signup', views.signup_page, name="signup"),
    path('register-user', views.register, name="register"),
    path('login-user', views.login, name="login"),
    path('checkout', views.checkout_page, name="checkout-prev"),
]

