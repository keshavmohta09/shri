from django.urls import path

from .views import (
    create_product_email,
    get_about,
    get_terms_and_conditions,
    home,
)

urlpatterns = [
    path("", home, name="home-page"),
    path("product-emails/", create_product_email, name="create-product-email"),
    path("about/", get_about, name="about"),
    path("conditions/", get_terms_and_conditions, name="terms_and_conditions"),
]
