from django.core.management import call_command
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "اگر فروشگاه خالی باشد، فهرست محصولات را یک‌بار بارگذاری می‌کند."

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write("catalog already present; skipping seed.")
            return
        call_command("seed_shop")
