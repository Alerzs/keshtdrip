import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "اگر DJANGO_SUPERUSER_USERNAME تازه باشد، یک مدیر کل می‌سازد."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME is unset; skipping.")
            return
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"{username} already exists; password and role left unchanged.")
            return
        user = User.objects.create_superuser(
            username=username,
            email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
            password=password,
        )
        name = os.environ.get("DJANGO_SUPERUSER_NAME", "").strip()
        if name:
            user.first_name = name
            user.save(update_fields=["first_name"])
        self.stdout.write(self.style.SUCCESS(f"Created superuser {username}."))
