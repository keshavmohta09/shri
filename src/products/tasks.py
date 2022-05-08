from celery import shared_task
from django.db import IntegrityError
from helpers.constants import OBJECT_NOT_FOUND
from helpers.functions import send_email
from products.functions import extract_information_from_url
from django.core.exceptions import ValidationError

from products.models import Product, ProductEmail
from django.utils.timezone import now
from datetime import datetime, timedelta


@shared_task()
def send_email_on_update_product_task():
    message = """Subject: Price updates from SHRI
Hello,

This is to inform you that the price of {title} is {incr_or_dcr}.

The link of the product: 
{url}.

    
Thankyou!
Team Shri
"""

    products = tuple(Product.objects.all())
    product_list = []

    for product in products:
        extract_data = extract_information_from_url(url=product.url)
        if product.current_price != extract_data["price"]:
            product.current_price, product.previous_price = (
                extract_data["price"],
                product.current_price,
            )
            product_list.append(product)

    try:
        Product.objects.bulk_update(
            objs=product_list, fields=("current_price", "previous_price")
        )
    except IntegrityError as error:
        print("========================", error, "=================================")

    product_id_list = [product.id for product in product_list]

    product_emails = tuple(
        ProductEmail.objects.filter(
            product_id__in=product_id_list, date_deleted__isnull=True
        )
    )
    receiver_emails = []
    update_product_email_list = []
    for product_email in product_emails:
        if (
            product_email.date_created + timedelta(days=product_email.days_limit)
            < now()
        ):
            product_email.date_deleted = now()
            update_product_email_list.append(product_email)
        else:
            receiver_emails.append(product_email.email)

        send_email(
            receivers=receiver_emails,
            message=message.format(
                title=product_email.product.title,
                url=product_email.product.url,
                incr_or_dcr="increased"
                if product.current_price > product.previous_price
                else "decreased",
            ).encode("utf-8"),
        )

    try:
        ProductEmail.objects.bulk_update(
            objs=update_product_email_list, fields=("date_deleted",)
        )
    except IntegrityError as error:
        print("========================", error, "=================================")
