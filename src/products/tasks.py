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
    print("++++++++++++++++++++++++++++++++++++++++++++++")
    # message = f"""
    # Subject: Price updates on {product.title} from SHRI
    # Hello,
    # This is to inform you that the price of {product.title} is {"increased" if product.previous_price<product.current_price else "decreased"}.
    # The link of the product: {product.url}.

    # Thankyou!
    # """
    message = "aaaaaaaaaaaaaaaaaaaaaa"

    products = tuple(Product.objects.all())
    product_id_list = []

    for product in products:
        extract_data = extract_information_from_url(url=product.url)
        if product.current_price != extract_data["price"]:
            product.current_price, product.previous_price = (
                extract_data["price"],
                product.current_price,
            )
            try:
                product.save(update_fields=("current_price", "previous_price"))
            except ValidationError as error:
                print("=============", str(error), "=============")
                continue
            product_id_list.append(product.id)

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
            <= now()
        ):
            product_email.date_deleted = now()
            update_product_email_list.append(product_email)
        else:
            receiver_emails.append(product_email.email)

    try:
        s = ProductEmail.objects.bulk_update(
            objs=update_product_email_list, fields=("date_deleted",)
        )
        print(s)
    except IntegrityError as error:
        print("========================", error, "=================================")

    send_email(receivers=receiver_emails, message=message)
