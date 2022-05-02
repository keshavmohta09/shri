from django.urls import path

from .views import create_product_email, home

urlpatterns = [
    path("", home, name="home-page"),
    path("product-emails/", create_product_email, name="create-product-email"),
]
