from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from . import cart as cart_store
from .blog_posts import all_posts, get_post
from .models import Brand, Category, Product

SHOWCASE_IMAGES = [
    "img/showcase/01.svg",
    "img/showcase/02.svg",
    "img/showcase/03.svg",
    "img/showcase/04.svg",
    "img/showcase/05.svg",
    "img/showcase/06.svg",
]


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


def _cart_items(session):
    raw = cart_store.get_cart(session)
    products = Product.objects.filter(id__in=raw.keys()).select_related("category", "brand")
    items = []
    total = 0
    for product in products:
        qty = raw[str(product.id)]
        line = product.price * qty
        total += line
        max_choice = min(max(product.stock, qty), 10)
        qty_list = list(range(1, max_choice + 1))
        if qty not in qty_list:
            qty_list.append(qty)
            qty_list.sort()
        items.append(
            {
                "product": product,
                "quantity": qty,
                "line_total": line,
                "qty_list": qty_list,
            }
        )
    return items, total


def home(request):
    categories = list(Category.objects.all())
    featured = Product.objects.filter(featured=True).select_related("category", "brand")
    fresh = Product.objects.select_related("category", "brand").order_by("-created_at")[:12]
    showcase = []
    for i, cat in enumerate(categories):
        image_url = cat.image.url if cat.image else static(SHOWCASE_IMAGES[i % len(SHOWCASE_IMAGES)])
        showcase.append({"category": cat, "image_url": image_url})
    return render(
        request,
        "shop/home.html",
        {
            "categories": categories,
            "featured": featured,
            "fresh": fresh,
            "showcase": showcase,
            "drips": Product.objects.filter(category__slug="irrigation"),
            "joints": Product.objects.filter(category__slug="joints"),
            "blog_posts": all_posts(),
        },
    )


def catalog(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.select_related("category", "brand")
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
    return render(
        request,
        "shop/catalog.html",
        {
            "categories": categories,
            "brands": brands,
            "products": products,
            "active_category": active,
            "active_brand": active_brand,
            "query": q,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "brand").prefetch_related("images"),
        slug=slug,
    )
    related = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.pk)
        .select_related("category", "brand")[:4]
    )
    return render(
        request,
        "shop/product.html",
        {"product": product, "related": related, "gallery": _product_gallery(product)},
    )


@require_POST
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    qty = max(1, int(request.POST.get("quantity", 1)))
    cart_store.add_item(request.session, product.id, qty)
    messages.success(request, f"«{product.name}» به سبد خرید افزوده شد.")
    next_url = request.POST.get("next") or product.get_absolute_url()
    return redirect(next_url)


@require_POST
def update_cart(request, product_id):
    qty = int(request.POST.get("quantity", 1))
    cart_store.set_quantity(request.session, product_id, qty)
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_store.remove_item(request.session, product_id)
    return redirect("cart")


def cart_view(request):
    items, total = _cart_items(request.session)
    in_cart_ids = [item["product"].id for item in items]
    featured = (
        Product.objects.filter(featured=True, stock__gt=0)
        .exclude(id__in=in_cart_ids)
        .select_related("category", "brand")
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
