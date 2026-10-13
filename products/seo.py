import json
from urllib.parse import urlencode
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .blog_posts import all_posts
from .models import Brand, Category, Product

SITE_NAME = "کشت‌دریپ"
HOME_TITLE = "خرید نوار تیپ و لوازم آبیاری | کشت‌دریپ"
HOME_HEADING = "خرید نوار تیپ و لوازم آبیاری قطره‌ای"
HOME_DESCRIPTION = (
    "خرید نوار تیپ پلاکدار و درزدار با قیمت روز. "
    "لوازم آبیاری قطره‌ای، مشاوره رایگان و ارسال سریع به سراسر ایران."
)
HOME_INTRO = (
    "نوار تیپ پلاکدار و درزدار، لوله، فیلتر و اتصالات را برای آبیاری قطره‌ای "
    "با قیمت روز و مشخصات فنی شفاف از کشت‌دریپ سفارش دهید."
)
TAPE_TITLE = "خرید نوار تیپ | کشت‌دریپ"
TAPE_DESCRIPTION = (
    "خرید نوار تیپ پلاکدار و درزدار در فاصله ۱۰، ۲۰ و ۳۰ سانتی‌متر. "
    "قیمت روز نوار تیپ، مشاوره انتخاب ضخامت و ارسال به سراسر ایران."
)
SHOP_TITLE = "خرید لوازم آبیاری | کشت‌دریپ"
SHOP_DESCRIPTION = (
    "خرید لوازم آبیاری قطره‌ای از کشت‌دریپ: نوار تیپ، لوله پلی‌اتیلن، لوله نخدار، "
    "فیلتر و اتصالات. قیمت به‌روز و ارسال به سراسر ایران."
)
PRIVATE_DESCRIPTION = "این صفحه بخشی از فرآیند خرید کشت‌دریپ است و برای نمایه‌سازی موتورهای جستجو نیست."

NOINDEX = {"cart", "checkout", "account", "logout", "add_to_cart", "update_cart", "remove_from_cart"}


def clip(text, limit):
    text = " ".join(str(text or "").split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return (cut or text[:limit]).rstrip("،. ") + "…"


def absolute_url(request, path):
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    site = getattr(settings, "SITE_URL", "") or ""
    if site:
        return site.rstrip("/") + path
    return request.build_absolute_uri(path)


def _json(data):
    raw = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return mark_safe(raw)


def _graph(request, extra=None):
    site = absolute_url(request, "/")
    graph = [
        {
            "@type": "OnlineStore",
            "@id": site + "#store",
            "name": SITE_NAME,
            "url": site,
            "description": HOME_DESCRIPTION,
            "areaServed": "IR",
            "inLanguage": "fa",
        },
        {
            "@type": "WebSite",
            "@id": site + "#website",
            "name": SITE_NAME,
            "url": site,
            "inLanguage": "fa",
            "publisher": {"@id": site + "#store"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": absolute_url(request, reverse("catalog")) + "?q={search_term_string}",
                "query-input": "required name=search_term_string",
            },
        },
    ]
    if extra:
        graph.extend(extra)
    return _json({"@context": "https://schema.org", "@graph": graph})


def pack(request, *, title, description, robots="index, follow", canonical=None, image="", og_type="website", extra_graph=None, heading="", intro="", keywords="", published="", modified="", section=""):
    data = {
        "title": clip(title, 70),
        "description": clip(description, 160),
        "robots": robots,
        "canonical": canonical or absolute_url(request, request.path),
        "image": image,
        "og_type": og_type,
        "json_ld": _graph(request, extra_graph),
        "heading": heading,
        "intro": intro,
    }
    if keywords:
        data["keywords"] = keywords
    if published:
        data["published"] = published
    if modified:
        data["modified"] = modified
    if section:
        data["section"] = section
    return data


def _crumbs(request, items):
    elements = []
    for index, (name, url) in enumerate(items, start=1):
        element = {"@type": "ListItem", "position": index, "name": name}
        if url:
            element["item"] = url
        elements.append(element)
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def seo_for_request(request):
    match = getattr(request, "resolver_match", None)
    name = match.url_name if match else "home"
    if name in NOINDEX:
        labels = {
            "cart": "سبد خرید",
            "checkout": "ثبت سفارش",
            "account": "حساب کاربری",
            "logout": "خروج",
        }
        title = f"{labels.get(name, 'کشت‌دریپ')} | کشت‌دریپ"
        return pack(request, title=title, description=PRIVATE_DESCRIPTION, robots="noindex, follow")
    if name == "about":
        return pack(
            request,
            title="درباره کشت‌دریپ | خرید لوازم آبیاری",
            description="کشت‌دریپ تأمین‌کننده نوار تیپ و لوازم آبیاری قطره‌ای است. مشاوره پیش از خرید، ضمانت اصالت و ارسال به سراسر ایران.",
            heading="درباره کشت‌دریپ",
        )
    if name == "blog":
        return blog_list_seo(request, all_posts())
    if name == "home_amp":
        return pack(
            request,
            title=HOME_TITLE,
            description=HOME_DESCRIPTION,
            canonical=absolute_url(request, reverse("home")),
            image=absolute_url(request, "/static/img/drip-banner.png"),
            heading=HOME_HEADING,
            intro=HOME_INTRO,
        )
    seo = pack(
        request,
        title=HOME_TITLE,
        description=HOME_DESCRIPTION,
        image=absolute_url(request, "/static/img/drip-banner.png"),
        heading=HOME_HEADING,
        intro=HOME_INTRO,
    )
    if name == "home":
        seo["amphtml"] = absolute_url(request, reverse("home_amp"))
    return seo


def catalog_seo(request, *, category, brand, query, products):
    params = {}
    if category:
        params["category"] = category.slug
    if brand:
        params["brand"] = brand.slug
    path = reverse("catalog")
    if params:
        path += "?" + urlencode(params)
    canonical = absolute_url(request, path)
    shop_url = absolute_url(request, reverse("catalog"))
    crumbs = [("خانه", absolute_url(request, reverse("home"))), ("خرید لوازم آبیاری", shop_url)]

    if query:
        seo = pack(
            request,
            title=f"جستجوی {query} | کشت‌دریپ",
            description=f"نتایج جستجو برای {query} در فروشگاه لوازم آبیاری کشت‌دریپ.",
            robots="noindex, follow",
            canonical=shop_url,
            heading=f"جستجو: {query}",
            intro="",
        )
        return seo

    if category and category.slug == "drip-tape":
        title = TAPE_TITLE
        description = TAPE_DESCRIPTION
        heading = "خرید نوار تیپ"
        intro = "نوار تیپ پلاکدار و درزدار، با فاصله قطره‌چکان ۱۰، ۲۰ و ۳۰ سانتی‌متر. برای خرید نوار تیپ، ضخامت و فاصله خروجی را با نوع کشت و طول ردیف انتخاب کنید."
    elif category and brand:
        title = f"خرید {category.name} {brand.name} | کشت‌دریپ"
        description = f"خرید {category.name} برند {brand.name} از فروشگاه لوازم آبیاری کشت‌دریپ. {category.tagline}"
        heading = f"خرید {category.name} {brand.name}"
        intro = category.tagline
    elif category:
        title = f"خرید {category.name} | لوازم آبیاری کشت‌دریپ"
        description = f"خرید {category.name} از کشت‌دریپ. {category.tagline} ارسال لوازم آبیاری به سراسر ایران."
        heading = f"خرید {category.name}"
        intro = category.tagline
    elif brand:
        title = f"محصولات {brand.name} | خرید لوازم آبیاری"
        description = f"خرید لوازم آبیاری برند {brand.name}، از جمله نوار تیپ، لوله و اتصالات، از کشت‌دریپ."
        heading = brand.name
        intro = f"محصولات برند {brand.name} در فروشگاه لوازم آبیاری کشت‌دریپ."
    else:
        title = SHOP_TITLE
        description = SHOP_DESCRIPTION
        heading = "خرید لوازم آبیاری"
        intro = "نوار تیپ، لوله پلی‌اتیلن، لوله نخدار و اتصالات آبیاری قطره‌ای را با مشخصات فنی شفاف مقایسه و سفارش دهید."

    if category:
        crumbs.append((category.name, absolute_url(request, category.get_absolute_url())))
    if brand:
        crumbs.append((brand.name, None))

    extra = [
        _crumbs(request, crumbs),
        {
            "@type": "ItemList",
            "name": heading,
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": product.name,
                    "url": absolute_url(request, product.get_absolute_url()),
                }
                for index, product in enumerate(products[:24], start=1)
            ],
        },
    ]
    return pack(
        request,
        title=title,
        description=description,
        canonical=canonical,
        extra_graph=extra,
        heading=heading,
        intro=intro,
    )


def product_seo(request, product, *, price, image="", sku=""):
    description = product.blurb or product.description
    description = f"خرید {product.name} از کشت‌دریپ. {description}"
    url = absolute_url(request, product.get_absolute_url())
    images = [image] if image else []
    offer = {
        "@type": "Offer",
        "url": url,
        "priceCurrency": "IRR",
        "price": int(price) * 10,
        "availability": "https://schema.org/InStock" if product.stock else "https://schema.org/OutOfStock",
        "itemCondition": "https://schema.org/NewCondition",
    }
    product_node = {
        "@type": "Product",
        "name": product.name,
        "description": clip(description, 300),
        "sku": sku or product.slug,
        "url": url,
        "brand": {"@type": "Brand", "name": product.brand.name},
        "category": product.category.name,
        "offers": offer,
    }
    if images:
        product_node["image"] = images
    crumbs = _crumbs(
        request,
        [
            ("خانه", absolute_url(request, reverse("home"))),
            ("خرید لوازم آبیاری", absolute_url(request, reverse("catalog"))),
            (product.category.name, absolute_url(request, product.category.get_absolute_url())),
            (product.name, url),
        ],
    )
    return pack(
        request,
        title=f"خرید {product.name} | کشت‌دریپ",
        description=description,
        canonical=url,
        image=image,
        extra_graph=[product_node, crumbs],
    )


def _schema_datetime(value):
    value = str(value or "")[:10]
    if len(value) == 10 and value[4] == "-" and value[7] == "-":
        return value + "T08:00:00+03:30"
    return ""


def post_lastmod(post):
    return str(post.get("updated") or post.get("published") or "")[:10]


def blog_list_seo(request, posts):
    url = absolute_url(request, reverse("blog"))
    description = (
        "آموزش انتخاب نوار تیپ، تنظیم فشار و طول ردیف، فیلتراسیون، کودآبیاری و نگهداری سامانه قطره‌ای. "
        "راهنمای عملی کشت‌دریپ برای مزرعه، باغ و گلخانه."
    )
    graph = [
        {
            "@type": "Blog",
            "@id": url + "#blog",
            "name": "وبلاگ کشت‌دریپ",
            "description": description,
            "url": url,
            "inLanguage": "fa",
            "publisher": {"@id": absolute_url(request, "/") + "#store"},
        },
        {
            "@type": "ItemList",
            "name": "مقاله‌های آبیاری قطره‌ای",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": post["title"],
                    "url": absolute_url(request, reverse("blog_detail", kwargs={"slug": post["slug"]})),
                }
                for index, post in enumerate(posts, start=1)
            ],
        },
        _crumbs(
            request,
            [
                ("خانه", absolute_url(request, reverse("home"))),
                ("وبلاگ", url),
            ],
        ),
    ]
    return pack(
        request,
        title="راهنمای آبیاری قطره‌ای و نوار تیپ | کشت‌دریپ",
        description=description,
        canonical=url,
        extra_graph=graph,
        heading="راهنمای آبیاری قطره‌ای و نوار تیپ",
        keywords="آبیاری قطره‌ای، نوار تیپ، فیلتر آبیاری، کودآبیاری، لوله پلی‌اتیلن",
    )


def blog_seo(request, post):
    url = absolute_url(request, reverse("blog_detail", kwargs={"slug": post["slug"]}))
    image = absolute_url(request, "/static/" + post["image"]) if post.get("image") else ""
    published = _schema_datetime(post.get("published"))
    modified = _schema_datetime(post.get("updated") or post.get("published"))
    keywords = [item for item in post.get("keywords") or [] if item]
    description = post.get("meta_description") or post["excerpt"]
    article = {
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": description,
        "inLanguage": "fa",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Organization", "name": SITE_NAME, "url": absolute_url(request, "/")},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
        "articleSection": post.get("category") or "آموزش آبیاری",
    }
    if published:
        article["datePublished"] = published
    if modified:
        article["dateModified"] = modified
    if image:
        article["image"] = image
    if keywords:
        article["keywords"] = "، ".join(keywords)
    crumbs = _crumbs(
        request,
        [
            ("خانه", absolute_url(request, reverse("home"))),
            ("وبلاگ", absolute_url(request, reverse("blog"))),
            (post["title"], url),
        ],
    )
    extra = [article, crumbs]
    faqs = post.get("faqs") or []
    if faqs:
        extra.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                    }
                    for item in faqs
                ],
            }
        )
    return pack(
        request,
        title=post.get("seo_title") or f"{post['title']} | کشت‌دریپ",
        description=description,
        canonical=url,
        image=image,
        og_type="article",
        extra_graph=extra,
        keywords="، ".join(keywords),
        published=published,
        modified=modified,
        section=post.get("category") or "",
    )


def attach(request, seo):
    request.seo = seo


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /account/",
        "Disallow: /basket/",
        "Disallow: /checkout/",
        f"Sitemap: {absolute_url(request, reverse('sitemap'))}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    posts = all_posts()
    blog_dates = [post_lastmod(post) for post in posts if post_lastmod(post)]
    entries = [
        (absolute_url(request, reverse("home")), "1.0", ""),
        (absolute_url(request, reverse("catalog")), "0.9", ""),
        (absolute_url(request, reverse("about")), "0.4", ""),
        (absolute_url(request, reverse("blog")), "0.8", max(blog_dates) if blog_dates else ""),
    ]
    for category in Category.objects.all():
        priority = "0.9" if category.slug == "drip-tape" else "0.7"
        entries.append((absolute_url(request, category.get_absolute_url()), priority, ""))
    for brand in Brand.objects.all():
        entries.append((absolute_url(request, brand.get_absolute_url()), "0.5", ""))
    for product in Product.objects.all().only("slug"):
        entries.append((absolute_url(request, product.get_absolute_url()), "0.8", ""))
    for post in posts:
        entries.append(
            (
                absolute_url(request, reverse("blog_detail", kwargs={"slug": post["slug"]})),
                "0.7",
                post_lastmod(post),
            )
        )

    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, lastmod in entries:
        body.append("  <url>")
        body.append(f"    <loc>{escape(loc)}</loc>")
        if lastmod:
            body.append(f"    <lastmod>{escape(lastmod)}</lastmod>")
        body.append(f"    <priority>{priority}</priority>")
        body.append("  </url>")
    body.append("</urlset>")
    return HttpResponse("\n".join(body), content_type="application/xml; charset=utf-8")
