from django.urls import path
from . import views

app_name = "adminview"
urlpatterns = [
    path('/', views.admin_page, name="admin-home"),
    path('add-product', views.add_product, name="add-product"),
]