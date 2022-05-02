from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from helpers.exceptions import RollbackException

from products.functions import extract_information_from_url

from .models import Product, ProductEmail


def home(request):
    return render(
        request=request,
        template_name="home.html",
        context={"days_limit": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    )


def create_product_email(request):
    data = request.POST

    url = data.get("url")
    email = data.get("email")
    days_limit = data.get("days_limit")

    url_information = extract_information_from_url(url=url)
    title, price = url_information["title"], url_information["price"]

    try:
        with transaction.atomic():
            product, created = Product.objects.get_or_create(
                url=url,
                defaults={
                    "title": title,
                    "current_price": price,
                    "previous_price": price,
                },
            )
            if not created and product.current_price != price:
                product.current_price, product.previous_price = (
                    price,
                    product.current_price,
                )
                try:
                    product.save(update_fields=("current_price", "previous_price"))
                except ValidationError as error:
                    messages.error(request=request, message=str(error))
                    raise RollbackException(message=str(error))

            product_email = ProductEmail(
                product_id=product.id, email=email, days_limit=days_limit
            )

            try:
                product_email.save()
            except ValidationError as error:
                messages.error(request=request, message=str(error))
                raise RollbackException(message=str(error))
    except RollbackException as error:
        return redirect("home-page")

    return render(request=request, template_name="submit.html")
