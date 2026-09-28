from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from .models import Brand, Category, Product, ProductImage, ProductVariant
from .price_import import PriceImportError, build_price_workbook, import_price_workbook


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
    fields = ("slug", "working_pressure", "diameter", "price", "sort_order")


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
    change_list_template = "admin/products/product/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "import-prices/",
                self.admin_site.admin_view(self.import_prices_view),
                name="products_product_import_prices",
            ),
            path(
                "export-prices/",
                self.admin_site.admin_view(self.export_prices_view),
                name="products_product_export_prices",
            ),
        ]
        return custom + urls

    def import_prices_view(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied

        result = None
        form_error = ""
        if request.method == "POST":
            upload = request.FILES.get("file")
            if not upload:
                form_error = "فایل اکسل را انتخاب کنید."
            else:
                try:
                    result = import_price_workbook(upload)
                except PriceImportError as exc:
                    form_error = str(exc)
                else:
                    if result.errors:
                        messages.warning(request, result.summary())
                    else:
                        messages.success(request, result.summary())

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "ورود قیمت از اکسل",
            "form_error": form_error,
            "result": result,
        }
        return render(request, "admin/products/product/import_prices.html", context)

    def export_prices_view(self, request):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        workbook = build_price_workbook()
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="product-prices.xlsx"'
        workbook.save(response)
        return response

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(variant_total=Count("variants"))

    @admin.display(description="تنوع‌ها", ordering="variant_total")
    def variant_total(self, obj):
        return obj.variant_total
