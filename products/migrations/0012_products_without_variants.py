from django.db import migrations, models


def split_variants_into_products(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    ProductAttribute = apps.get_model("products", "ProductAttribute")
    ProductImage = apps.get_model("products", "ProductImage")

    parents = list(Product.objects.filter(variants__isnull=False).distinct())
    for parent in parents:
        variants = list(parent.variants.all())
        attributes = list(parent.attributes.all())
        images = list(parent.images.all())
        for variant in variants:
            bits = []
            if variant.diameter:
                bits.append(f"قطر {variant.diameter}")
            if variant.working_pressure:
                bits.append(f"فشار کاری {variant.working_pressure}")
            name = parent.name
            if bits:
                name = f"{parent.name} — {'، '.join(bits)}"
            product = Product.objects.create(
                category_id=parent.category_id,
                brand_id=parent.brand_id,
                name=name[:140],
                slug=variant.slug,
                blurb=parent.blurb,
                description=parent.description,
                price=variant.price,
                unit=parent.unit,
                badge=parent.badge,
                featured=variant.featured,
                image=parent.image,
            )
            order = 0
            if variant.diameter:
                ProductAttribute.objects.create(
                    product=product,
                    name="قطر",
                    value=variant.diameter[:40],
                    sort_order=order,
                )
                order += 1
            if variant.working_pressure:
                ProductAttribute.objects.create(
                    product=product,
                    name="فشار کاری",
                    value=variant.working_pressure[:40],
                    sort_order=order,
                )
                order += 1
            for attr in attributes:
                ProductAttribute.objects.create(
                    product=product,
                    name=attr.name,
                    value=attr.value,
                    sort_order=order,
                )
                order += 1
            for image in images:
                ProductImage.objects.create(
                    product=product,
                    image=image.image,
                    alt=image.alt,
                    sort_order=image.sort_order,
                )
        parent.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_productattribute"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(allow_unicode=True, max_length=80, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="featured",
            field=models.BooleanField(
                default=False,
                help_text="این محصول در ریل محصولات ویژه و پیشنهاد سبد نشان داده می‌شود.",
                verbose_name="ویژه",
            ),
        ),
        migrations.RunPython(split_variants_into_products, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="product",
            name="stock",
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.PositiveIntegerField(help_text="قیمت به تومان"),
        ),
        migrations.DeleteModel(
            name="ProductVariant",
        ),
    ]
