from django.db import migrations, models


def _variant_name(parent_name, variant):
    bits = []
    if variant.diameter:
        bits.append(f"قطر {variant.diameter}")
    if variant.working_pressure:
        bits.append(f"فشار کاری {variant.working_pressure}")
    if not bits:
        return parent_name[:140]
    return f"{parent_name} — {'، '.join(bits)}"[:140]


def _parked_slug(Product, pk, reserved):
    number = pk
    while True:
        candidate = f"zz-migrate-{number}"[:80]
        if candidate not in reserved and not Product.objects.filter(slug=candidate).exists():
            reserved.add(candidate)
            return candidate
        number += 1


def _available_slug(Product, slug):
    base = (slug or "product")[:80]
    candidate = base
    number = 2
    while Product.objects.filter(slug=candidate).exists():
        suffix = f"-{number}"
        candidate = f"{base[: 80 - len(suffix)]}{suffix}"
        number += 1
    return candidate


def _write_attributes(ProductAttribute, product, variant, attributes, clear):
    if clear:
        ProductAttribute.objects.filter(product_id=product.pk).delete()
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


def split_variants_into_products(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    ProductAttribute = apps.get_model("products", "ProductAttribute")
    ProductImage = apps.get_model("products", "ProductImage")

    parents = list(Product.objects.filter(variants__isnull=False).distinct())
    reserved = set()
    for parent in parents:
        parent._variants = list(parent.variants.all())
        parent._attributes = list(parent.attributes.all())
        parent._images = list(parent.images.all())
        parent._source_slug = parent.slug
        for variant in parent._variants:
            if variant.slug:
                reserved.add(variant.slug)
        # A variant often keeps the parent product code. Inserting another row
        # with that slug fails the unique constraint, so that variant stays on
        # the existing product.
        parent._keep = any(variant.slug == parent._source_slug for variant in parent._variants)

    for parent in parents:
        if parent._keep:
            continue
        parent.slug = _parked_slug(Product, parent.pk, reserved)
        parent.save(update_fields=["slug"])

    for parent in parents:
        keeper = next(
            (variant for variant in parent._variants if variant.slug == parent._source_slug),
            None,
        )
        source_name = parent.name
        for variant in parent._variants:
            name = _variant_name(source_name, variant)
            if keeper is not None and variant.pk == keeper.pk:
                parent.name = name
                parent.slug = parent._source_slug
                parent.price = variant.price
                parent.featured = variant.featured
                parent.save()
                _write_attributes(
                    ProductAttribute,
                    parent,
                    variant,
                    parent._attributes,
                    clear=True,
                )
                continue
            product = Product.objects.create(
                category_id=parent.category_id,
                brand_id=parent.brand_id,
                name=name,
                slug=_available_slug(Product, variant.slug or f"{parent._source_slug}-{variant.pk}"),
                blurb=parent.blurb,
                description=parent.description,
                price=variant.price,
                unit=parent.unit,
                badge=parent.badge,
                featured=variant.featured,
                image=parent.image,
            )
            _write_attributes(
                ProductAttribute,
                product,
                variant,
                parent._attributes,
                clear=False,
            )
            for image in parent._images:
                ProductImage.objects.create(
                    product=product,
                    image=image.image,
                    alt=image.alt,
                    sort_order=image.sort_order,
                )
        if keeper is None:
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
