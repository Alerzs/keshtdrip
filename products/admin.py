from django.contrib import admin

from .models import Brand, Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "alt", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "unit", "featured", "stock")
    list_filter = ("category", "brand", "featured")
    search_fields = ("name", "blurb")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
