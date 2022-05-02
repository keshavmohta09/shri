from django.contrib import admin

from products.models import Product, ProductEmail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "current_price", "previous_price", "url")
    search_fields = ("title", "url")


@admin.register(ProductEmail)
class ProductEmailAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "email", "days_limit")
    search_fields = ("email",)
    list_filter = ("days_limit",)
