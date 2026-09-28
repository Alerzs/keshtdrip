from django.db import migrations, models


def populate_variant_slugs(apps, schema_editor):
    ProductVariant = apps.get_model("products", "ProductVariant")
    for variant in ProductVariant.objects.select_related("product").order_by("id"):
        variant.slug = f"{variant.product.slug}-{variant.pk}"
        variant.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_category_showcase_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="slug",
            field=models.SlugField(allow_unicode=True, max_length=80, null=True, verbose_name="کد"),
        ),
        migrations.RunPython(populate_variant_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="productvariant",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                help_text="کد یکتای این تنوع. برای هر تنوع الزامی است.",
                max_length=80,
                unique=True,
                verbose_name="کد",
            ),
        ),
    ]
