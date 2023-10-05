from django.urls import path
from . import views

app_name = "adminview"
urlpatterns = [
    path('', views.admin_page, name="admin-home"),
    path('add-product/', views.add_product, name="add-product"),
    path('products/', views.admin_page, name="products"),
    path('analytics/', views.admin_page, name="analytics"),
    path("<str:prodid>/edit-product/", views.edit_product_details, name="edit-product-details"),
    path("<str:prodid>/update-product/", views.update_product, name="update_product"),
    path("<str:prodid>/delete-product/", views.delete_product, name="delete-product"),
    path('logout-user/', views.logout_user, name="logout"),
]