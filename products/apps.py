# Django app config
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = "products"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from django.core.cache import cache
        from django.db.models.signals import post_delete, post_save

        from .models import Category, Product, ProductVariant

        def clear_home_cache(**kwargs):
            cache.delete("shop-home-v1")

        for model in (Category, Product, ProductVariant):
            post_save.connect(clear_home_cache, sender=model, dispatch_uid=f"clear-home-{model.__name__}")
            post_delete.connect(clear_home_cache, sender=model, dispatch_uid=f"clear-home-del-{model.__name__}")
