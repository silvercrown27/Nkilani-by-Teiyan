from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'userview'

urlpatterns = [
    path('home/', views.home_page, name="user-home"),
    path('contact/', views.contact_page, name="contact"),
    path('wishlist/', views.wishlist_page, name="user-wishlist"),
    path('<str:prodid>/', views.detail_page, name="prod-detail"),
    path('cart/', views.cart_page, name="user-cart"),
    path('shop/', views.shop_page, name="user-shop"),
    path('checkout/', views.checkout_page, name="user-checkout"),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('<str:prodid>-review/', views.add_review, name='add-review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
