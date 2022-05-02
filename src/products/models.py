from django.core.exceptions import ValidationError
from django.db import models
from helpers.models import BaseModel

from products.constants import MAXIMUM_DAYS_LIMIT_REACHED


class Product(BaseModel):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=2083, unique=True)
    current_price = models.FloatField()
    previous_price = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductEmail(BaseModel):
    MAX_DAYS_LIMIT = 10

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    email = models.CharField(max_length=320)
    days_limit = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Product Email"
        verbose_name_plural = "Product Emails"
        unique_together = (("product_id", "email", "date_deleted"),)

    def validate_days_limit(self):
        if self.days_limit > self.MAX_DAYS_LIMIT:
            raise ValidationError(MAXIMUM_DAYS_LIMIT_REACHED)

    def clean(self):
        self.validate_days_limit()
