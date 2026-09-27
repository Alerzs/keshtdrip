from django.contrib import admin
from django.db.models import Count

from .models import Brand, Category, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    fields = ("name", "slug", "tagline", "image", "showcase_image")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("working_pressure", "diameter", "price", "sort_order")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "alt", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "variant_total", "unit", "featured", "stock")
    list_filter = ("category", "brand", "featured")
    search_fields = ("name", "blurb")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline, ProductImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(variant_total=Count("variants"))

    @admin.display(description="تنوع‌ها", ordering="variant_total")
    def variant_total(self, obj):
        return obj.variant_total
