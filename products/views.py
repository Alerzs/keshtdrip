from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from . import cart as cart_store
from .blog_posts import all_posts, featured_posts, get_post, grouped_posts, related_posts
from .images import image_fit, image_src, sibling_image_urls
from .models import Brand, Category, Product
from .seo import PRIVATE_DESCRIPTION, absolute_url, attach, blog_seo, catalog_seo, pack, product_seo


def _dedupe_alts(items):
    totals = {}
    for item in items:
        totals[item["alt"]] = totals.get(item["alt"], 0) + 1
    seen = {}
    for item in items:
        base = item["alt"]
        if totals[base] < 2:
            continue
        seen[base] = seen.get(base, 0) + 1
        item["alt"] = f"{base} — نمای {seen[base]}"


def _product_gallery(product):
    items = []
    seen = set()

    def add(url, alt):
        url = image_src(url)
        if url and url not in seen:
            seen.add(url)
            text = " ".join(str(alt or "").split()) or product.name or "تصویر محصول"
            items.append({"url": url, "alt": text})

    if product.image:
        add(product.image, product.name)
    for extra in product.images.all():
        if extra.image:
            add(extra.image, extra.alt or product.name)
    if len(items) < 2:
        for url in sibling_image_urls(product.image):
            add(url, f"{product.name} — نمای {len(items) + 1}")
    _dedupe_alts(items)
    return items


def _catalog(qs=None):
    products = qs if qs is not None else Product.objects.all()
    return products.select_related("category", "brand").prefetch_related("attributes")


def _cart_items(session):
    raw = cart_store.get_cart(session)
    merged = {}
    for key, qty in raw.items():
        try:
            product_id = cart_store.parse_line_key(key)
            quantity = int(qty)
        except (TypeError, ValueError):
            continue
        if quantity < 1:
            continue
        merged[product_id] = merged.get(product_id, 0) + quantity
    products = {
        product.id: product
        for product in Product.objects.filter(id__in=merged)
        .select_related("category", "brand")
        .prefetch_related("attributes")
    }
    items = []
    total = 0
    cleaned = {}
    for product_id, qty in merged.items():
        product = products.get(product_id)
        if product is None:
            continue
        unit_price = product.price
        line = unit_price * qty
        total += line
        qty_list = list(range(1, 11))
        if qty not in qty_list:
            qty_list.append(qty)
            qty_list.sort()
        key = str(product_id)
        cleaned[key] = qty
        items.append(
            {
                "key": key,
                "product": product,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line,
                "qty_list": qty_list,
            }
        )
    if cleaned != {str(key): value for key, value in raw.items()}:
        cart_store.save_cart(session, cleaned)
    return items, total


def _featured_products(in_cart_ids=None):
    products = Product.objects.filter(featured=True).select_related("category", "brand").prefetch_related("attributes")
    if in_cart_ids is not None:
        products = products.exclude(id__in=in_cart_ids)
    return products.order_by("name", "id")


HOME_CACHE_KEY = "shop-home-v2"
HOME_RAIL_LIMIT = 12


def _home_rail(qs):
    return list(qs[:HOME_RAIL_LIMIT])


def home_amp(request):
    return render(
        request,
        "shop/home_amp.html",
        {
            "categories": Category.objects.all()[:8],
            "blog_posts": featured_posts(6),
        },
    )


def home(request):
    try:
        payload = cache.get(HOME_CACHE_KEY)
    except Exception:
        cache.delete(HOME_CACHE_KEY)
        payload = None
    if payload is None:
        categories = list(Category.objects.all())
        payload = {
            "categories": categories,
            "featured": _home_rail(_featured_products()),
            "fresh": _home_rail(_catalog().order_by("-created_at")),
            "showcase": [
                {"category": cat, "image_url": image_fit(cat.showcase_image, 1280)}
                for cat in categories
                if cat.showcase_image
            ],
            "pipes": _home_rail(_catalog(Product.objects.filter(category__slug="layflat"))),
            "tapes": _home_rail(_catalog(Product.objects.filter(category__slug="drip-tape"))),
            "blog_posts": featured_posts(6),
        }
        cache.set(HOME_CACHE_KEY, payload, 120)
    return render(request, "shop/home.html", payload)


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
        Product.objects.select_related("category", "brand").prefetch_related("images", "attributes"),
        slug=slug,
    )
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
            price=product.price,
            image=image,
            sku=product.slug,
        ),
    )
    return render(
        request,
        "shop/product.html",
        {
            "product": product,
            "related": related,
            "gallery": gallery,
        },
    )


@require_POST
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)
    cart_store.add_item(request.session, product.id, qty)
    messages.success(request, f"«{product.name}» به سبد خرید افزوده شد.")
    next_url = request.POST.get("next") or product.get_absolute_url()
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
    featured = _featured_products(in_cart_ids)
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
    return render(request, "shop/blog.html", {"groups": grouped_posts(), "post_count": len(all_posts())})


def blog_detail(request, slug):
    post = get_post(slug)
    if not post:
        return redirect("blog")
    attach(request, blog_seo(request, post))
    return render(
        request,
        "shop/blog_post.html",
        {"post": post, "related": related_posts(post)},
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
