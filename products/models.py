from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, allow_unicode=True)
    tagline = models.CharField(max_length=160)
    image = models.CharField(
        "آدرس تصویر",
        max_length=300,
        blank=True,
        help_text="آدرس مستقیم فایل در static. مثال: /static/img/categories/drip-tape.svg",
    )
    showcase_image = models.CharField(
        "آدرس تصویر ویترین",
        max_length=300,
        blank=True,
        help_text="آدرس مستقیم اسلاید صفحه اصلی در static. جدا از تصویر کارت دسته است.",
    )

    class Meta:
        verbose_name = "دسته"
        verbose_name_plural = "دسته‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog") + f"?category={self.slug}"


class Brand(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog") + f"?brand={self.slug}"


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True)
    blurb = models.CharField(max_length=220)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="قیمت به تومان")
    unit = models.CharField(max_length=40, default="عدد")
    brand = models.ForeignKey("Brand", related_name="products", on_delete=models.PROTECT)
    badge = models.CharField(
        "برچسب",
        max_length=40,
        blank=True,
        help_text="متن کوتاه روی کارت محصول. مثال: پرفروش",
    )
    featured = models.BooleanField(
        "ویژه",
        default=False,
        help_text="این محصول در ریل محصولات ویژه و پیشنهاد سبد نشان داده می‌شود.",
    )
    image = models.CharField(
        "آدرس تصویر",
        max_length=300,
        blank=True,
        help_text="آدرس مستقیم فایل در static. مثال: /static/img/products/KSH-P-00000002.svg",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)
    name = models.CharField("عنوان", max_length=40, help_text="مثال: طول")
    value = models.CharField("مقدار", max_length=40, help_text="مثال: 1000 متر")
    sort_order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.name} {self.value}"

    def save(self, *args, **kwargs):
        self.name = (self.name or "").strip()
        self.value = (self.value or "").strip()
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.CharField(
        "آدرس تصویر",
        max_length=300,
        help_text="آدرس مستقیم فایل در static. مثال: /static/img/products/KSH-P-00000002-2.svg",
    )
    alt = models.CharField("عنوان تصویر", max_length=140, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.alt or f"تصویر {self.pk}"
