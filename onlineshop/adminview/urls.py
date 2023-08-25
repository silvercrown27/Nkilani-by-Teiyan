from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_page, name="landing_page"),
    path('add-product/', views.add_product, name="add-product"),
]