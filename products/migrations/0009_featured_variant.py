from django.db import migrations, models


def copy_featured_to_first_variant(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    ProductVariant = apps.get_model("products", "ProductVariant")
    for product in Product.objects.filter(featured=True):
        variant = ProductVariant.objects.filter(product=product).order_by("sort_order", "id").first()
        if variant is None:
            continue
        variant.featured = True
        variant.save(update_fields=["featured"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0008_image_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="featured",
            field=models.BooleanField(
                default=False,
                help_text="این تنوع در ریل محصولات مرتبط نشان داده می‌شود. برای هر محصول فقط یک تنوع ویژه است.",
                verbose_name="ویژه",
            ),
        ),
        migrations.RunPython(copy_featured_to_first_variant, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="product",
            name="featured",
        ),
    ]
