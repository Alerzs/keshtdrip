from django.db import migrations, models
import django.db.models.deletion


BRANDS = [
    ("کشت‌دریپ", "keshtdrip"),
    ("پارت الکتریک", "part-electric"),
    ("زردشت", "zardasht"),
    ("پارس بذر", "pars-seed"),
    ("البرز خاک", "alborz-soil"),
    ("لالجین سفال", "laljin"),
    ("مس زنجان", "zanjan-copper"),
    ("ساوه نهال", "saveh-nursery"),
]


def assign_brands(apps, schema_editor):
    Brand = apps.get_model("products", "Brand")
    Product = apps.get_model("products", "Product")
    brands = {
        slug: Brand.objects.create(name=name, slug=slug) for name, slug in BRANDS
    }
    default = brands["keshtdrip"]
    for product in Product.objects.all():
        haystack = f"{product.name} {product.origin or ''}"
        if any(token in haystack for token in ("زردشت", "کود", "اوره", "جلبک", "گل‌دهی", "گلدهي")):
            brand = brands["zardasht"]
        elif any(token in haystack for token in ("بذر", "گوجه", "زعفران", "شهد")):
            brand = brands["pars-seed"]
        elif any(token in haystack for token in ("زهکش", "کمپوست", "کوکوپیت", "خاک")):
            brand = brands["alborz-soil"]
        elif any(token in haystack for token in ("نهال", "انجیر", "انار")):
            brand = brands["saveh-nursery"]
        elif "کوزه" in haystack or "لالجین" in haystack:
            brand = brands["laljin"]
        elif any(token in haystack for token in ("مسی", "قیچی", "جعبه", "زنجان")):
            brand = brands["zanjan-copper"]
        elif "پارت" in haystack or "برنج" in haystack:
            brand = brands["part-electric"]
        elif any(token in haystack for token in ("تیپ", "لوله", "دریپ", "گلخانه", "کندو")):
            brand = brands["keshtdrip"]
        else:
            brand = default
        product.brand = brand
        product.save(update_fields=["brand"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_productimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("slug", models.SlugField(allow_unicode=True, unique=True)),
            ],
            options={
                "verbose_name": "برند",
                "verbose_name_plural": "برندها",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="products.brand",
            ),
        ),
        migrations.RunPython(assign_brands, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="product",
            name="origin",
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="products.brand",
            ),
        ),
    ]
