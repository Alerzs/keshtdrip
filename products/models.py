from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, allow_unicode=True)
    tagline = models.CharField(max_length=160)
    image = models.ImageField(upload_to="categories/", blank=True)

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
    slug = models.SlugField(unique=True, allow_unicode=True)
    blurb = models.CharField(max_length=220)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="قیمت به تومان")
    unit = models.CharField(max_length=40, default="عدد")
    brand = models.ForeignKey("Brand", related_name="products", on_delete=models.PROTECT)
    badge = models.CharField(max_length=40, blank=True)
    stock = models.PositiveIntegerField(default=40)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    alt = models.CharField("عنوان تصویر", max_length=140, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.alt or f"تصویر {self.pk}"
