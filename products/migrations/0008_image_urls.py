from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_productvariant_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.CharField(
                blank=True,
                help_text="آدرس مستقیم فایل در static. مثال: /static/img/categories/drip-tape.svg",
                max_length=300,
                verbose_name="آدرس تصویر",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="showcase_image",
            field=models.CharField(
                blank=True,
                help_text="آدرس مستقیم اسلاید صفحه اصلی در static. جدا از تصویر کارت دسته است.",
                max_length=300,
                verbose_name="آدرس تصویر ویترین",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.CharField(
                blank=True,
                help_text="آدرس مستقیم فایل در static. مثال: /static/img/products/KSH-P-00000002.svg",
                max_length=300,
                verbose_name="آدرس تصویر",
            ),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.CharField(
                help_text="آدرس مستقیم فایل در static. مثال: /static/img/products/KSH-P-00000002-2.svg",
                max_length=300,
                verbose_name="آدرس تصویر",
            ),
        ),
    ]
