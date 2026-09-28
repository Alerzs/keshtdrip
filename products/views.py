from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from . import cart as cart_store
from .blog_posts import all_posts, get_post
from .models import Brand, Category, Product
from .seo import PRIVATE_DESCRIPTION, absolute_url, attach, blog_seo, catalog_seo, pack, product_seo


def _product_gallery(product):
    items = []
    seen = set()

    def add(url, alt):
        if url and url not in seen:
            seen.add(url)
            items.append({"url": url, "alt": alt})

    if product.image:
        add(product.image.url, product.name)
    for extra in product.images.all():
        if extra.image:
            add(extra.image.url, extra.alt or product.name)
    if len(items) < 2:
        for extra in _sibling_images(product):
            add(extra["url"], extra["alt"])
    return items


def _sibling_images(product):
    if not product.image:
        return []
    rel = Path(product.image.name)
    folder = Path(settings.MEDIA_ROOT) / rel.parent
    prefix = "".join(ch for ch in rel.stem if not ch.isdigit())
    if not prefix or not folder.is_dir():
        return []
    extras = []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        stem = "".join(ch for ch in path.stem if not ch.isdigit())
        if stem != prefix:
            continue
        stored = (rel.parent / path.name).as_posix()
        extras.append({"url": default_storage.url(stored), "alt": f"{product.name} — نمای {len(extras) + 1}"})
    return extras


def _catalog(qs=None):
    products = qs if qs is not None else Product.objects.all()
    return products.select_related("category", "brand").prefetch_related("variants")


def _unique_values(values):
    seen = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return seen


def _variant_payload(variants):
    return [
        {
            "id": variant.id,
            "slug": variant.slug,
            "working_pressure": variant.working_pressure,
            "diameter": variant.diameter,
            "price": variant.price,
        }
        for variant in variants
    ]


def _cart_items(session):
    raw = cart_store.get_cart(session)
    parsed = []
    product_ids = []
    for key, qty in raw.items():
        try:
            product_id, variant_id = cart_store.parse_line_key(key)
        except (TypeError, ValueError):
            continue
        product_ids.append(product_id)
        parsed.append((str(key), product_id, variant_id, qty))
    products = {
        product.id: product
        for product in Product.objects.filter(id__in=product_ids)
        .select_related("category", "brand")
        .prefetch_related("variants")
    }
    items = []
    total = 0
    cleaned = {}
    for key, product_id, variant_id, qty in parsed:
        product = products.get(product_id)
        if product is None:
            continue
        variant = None
        if variant_id is not None:
            variant = next((item for item in product.variants.all() if item.id == variant_id), None)
            if variant is None:
                continue
        unit_price = variant.price if variant else product.price
        line = unit_price * qty
        total += line
        max_choice = min(max(product.stock, qty), 10)
        qty_list = list(range(1, max_choice + 1))
        if qty not in qty_list:
            qty_list.append(qty)
            qty_list.sort()
        cleaned[key] = qty
        items.append(
            {
                "key": key,
                "product": product,
                "variant": variant,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line,
                "qty_list": qty_list,
            }
        )
    if len(cleaned) != len(raw):
        cart_store.save_cart(session, cleaned)
    return items, total


def home(request):
    categories = list(Category.objects.all())
    featured = _catalog(Product.objects.filter(featured=True))
    fresh = _catalog().order_by("-created_at")[:12]
    showcase = [
        {"category": cat, "image_url": cat.showcase_image.url}
        for cat in categories
        if cat.showcase_image
    ]
    return render(
        request,
        "shop/home.html",
        {
            "categories": categories,
            "featured": featured,
            "fresh": fresh,
            "showcase": showcase,
            "tapes": _catalog(Product.objects.filter(category__slug="drip-tape")),
            "drips": _catalog(Product.objects.filter(category__slug="irrigation")),
            "joints": _catalog(Product.objects.filter(category__slug="joints")),
            "blog_posts": all_posts(),
        },
    )


def catalog(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = _catalog()
    slug = request.GET.get("category")
    brand_slug = request.GET.get("brand")
    active = None
    active_brand = None
    if slug:
        active = get_object_or_404(Category, slug=slug)
        products = products.filter(category=active)
    if brand_slug:
        active_brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=active_brand)
    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(name__icontains=q)
    product_list = list(products)
    attach(request, catalog_seo(request, category=active, brand=active_brand, query=q, products=product_list))
    return render(
        request,
        "shop/catalog.html",
        {
            "categories": categories,
            "brands": brands,
            "products": product_list,
            "active_category": active,
            "active_brand": active_brand,
            "query": q,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "brand").prefetch_related("images", "variants"),
        slug=slug,
    )
    variants = list(product.variants.all())
    selected_variant = None
    requested = request.GET.get("variant", "").strip()
    if requested.isdigit():
        selected_variant = next((variant for variant in variants if variant.id == int(requested)), None)
    if selected_variant is None and variants:
        selected_variant = variants[0]
    related = _catalog(
        Product.objects.filter(category=product.category).exclude(pk=product.pk)
    )[:4]
    image = ""
    gallery = _product_gallery(product)
    if gallery:
        image = gallery[0]["url"]
        if image.startswith("/"):
            image = absolute_url(request, image)
    attach(
        request,
        product_seo(
            request,
            product,
            price=selected_variant.price if selected_variant else product.price,
            image=image,
            sku=selected_variant.slug if selected_variant else product.slug,
        ),
    )
    return render(
        request,
        "shop/product.html",
        {
            "product": product,
            "related": related,
            "gallery": gallery,
            "variants": variants,
            "pressures": _unique_values(variant.working_pressure for variant in variants),
            "diameters": _unique_values(variant.diameter for variant in variants),
            "selected_variant": selected_variant,
            "display_price": selected_variant.price if selected_variant else product.price,
            "variant_payload": _variant_payload(variants),
        },
    )


@require_POST
def add_to_cart(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("variants"), slug=slug)
    qty = max(1, int(request.POST.get("quantity", 1)))
    variants = list(product.variants.all())
    variant = None
    if variants:
        submitted_slug = (request.POST.get("variant_slug") or "").strip()
        if not submitted_slug:
            messages.error(request, "کد این تنوع ارسال نشده است.")
            return redirect(product.get_absolute_url())
        variant = next((item for item in variants if item.slug == submitted_slug), None)
        if variant is None:
            messages.error(request, "این تنوع موجود نیست.")
            return redirect(product.get_absolute_url())
    cart_store.add_item(request.session, product.id, qty, variant.id if variant else None)
    label = product.name
    if variant and variant.spec_label:
        label = f"{product.name} — {variant.spec_label}"
    messages.success(request, f"«{label}» به سبد خرید افزوده شد.")
    next_url = request.POST.get("next") or (
        variant.get_absolute_url() if variant else product.get_absolute_url()
    )
    return redirect(next_url)


@require_POST
def update_cart(request, line_key):
    qty = int(request.POST.get("quantity", 1))
    cart_store.set_quantity(request.session, line_key, qty)
    return redirect("cart")


@require_POST
def remove_from_cart(request, line_key):
    cart_store.remove_item(request.session, line_key)
    return redirect("cart")


def cart_view(request):
    items, total = _cart_items(request.session)
    in_cart_ids = [item["product"].id for item in items]
    featured = _catalog(
        Product.objects.filter(featured=True, stock__gt=0).exclude(id__in=in_cart_ids)
    )
    return render(
        request,
        "shop/cart.html",
        {
            "items": items,
            "total": total,
            "item_count": sum(item["quantity"] for item in items),
            "featured": featured,
        },
    )


def _safe_next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    return ""


def checkout(request):
    if not request.user.is_authenticated:
        messages.info(request, "برای ادامه خرید ابتدا وارد شوید یا ثبت‌نام کنید.")
        return redirect(f"{reverse('account')}?next={reverse('checkout')}")
    items, total = _cart_items(request.session)
    if request.method == "POST":
        if not items:
            messages.error(request, "سبد خرید خالی است.")
            return redirect("catalog")
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(request, "لطفاً نام گیرنده را وارد کنید.")
            return render(
                request,
                "shop/checkout.html",
                {"items": items, "total": total},
            )
        cart_store.clear_cart(request.session)
        attach(
            request,
            pack(
                request,
                title="سفارش ثبت شد | کشت‌دریپ",
                description=PRIVATE_DESCRIPTION,
                robots="noindex, follow",
            ),
        )
        return render(request, "shop/success.html", {"name": name, "total": total})
    if not items:
        messages.info(request, "پیش از ثبت سفارش، محصولی به سبد اضافه کنید.")
        return redirect("catalog")
    return render(request, "shop/checkout.html", {"items": items, "total": total})


def about(request):
    return render(request, "shop/about.html")


def blog_list(request):
    return render(request, "shop/blog.html", {"posts": all_posts()})


def blog_detail(request, slug):
    post = get_post(slug)
    if not post:
        return redirect("blog")
    attach(request, blog_seo(request, post))
    return render(
        request,
        "shop/blog_post.html",
        {"post": post, "posts": [p for p in all_posts() if p["slug"] != slug]},
    )


def account(request):
    next_url = _safe_next_url(request)
    if request.user.is_authenticated:
        if next_url:
            return redirect(next_url)
        return render(request, "shop/account.html")

    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if action == "login":
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
            else:
                login(request, user)
                return redirect(next_url or "account")
        elif action == "register":
            password2 = request.POST.get("password2", "")
            if not username or not password:
                messages.error(request, "نام کاربری و رمز عبور را وارد کنید.")
            elif password != password2:
                messages.error(request, "رمز عبور و تکرار آن یکسان نیست.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                messages.success(request, "حساب شما ساخته شد.")
                return redirect(next_url or "account")

    return render(request, "shop/account.html", {"next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید.")
    return redirect("home")
