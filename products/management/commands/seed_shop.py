from django.core.management.base import BaseCommand
from django.db import connection

from products.models import Brand, Category, Product, ProductVariant

CATEGORIES = [
    {
        "name": "کود شیمیایی",
        "slug": "chemical-fertilizer",
        "tagline": "کود پایه برای تغذیه مزرعه و باغ.",
        "image": "/static/img/categories/chemical-fertilizer.png",
        "showcase_image": "/static/img/head2.png",
    },
    {
        "name": "تجهیزات",
        "slug": "equipment",
        "tagline": "لوله باغی، مه پاش و نوار تیپ.",
        "image": "/static/img/head1.png",
        "showcase_image": "/static/img/head1.png",
    },
    {
        "name": "لوله پلی اتیلن",
        "slug": "pe-pipe",
        "tagline": "لوله پلی‌اتیلن در سایز و فشار کاری مختلف، فروش متری.",
        "image": "",
        "showcase_image": "",
    },
    {
        "name": "لوله نخدار",
        "slug": "layflat",
        "tagline": "لوله نخدار در سایزهای اینچی، رول صد متری.",
        "image": "/static/img/cat1.png",
        "showcase_image": "/static/img/cat1.png",
    },
    {
        "name": "نوار تیپ",
        "slug": "drip-tape",
        "tagline": "نوار تیپ آبیاری قطره ای طول 1000 متر",
        "image": "/static/img/driptape.png",
        "showcase_image": "/static/img/head3.png",
    },
]

BRANDS = [
    {
        "name": "کشت‌دریپ",
        "slug": "keshtdrip",
    },
    {
        "name": "خوشه چین",
        "slug": "خوشه-چین",
    },
]

PRODUCTS = [
    {
        "category": "chemical-fertilizer",
        "name": "کود اوره 50 کیلوگرم",
        "slug": "KSH-P-00000070",
        "image": "/static/img/fertelizer.jpg",
        "blurb": "کود اوره 50 کیلوگرم. واحد فروش: کیسه.",
        "description": "کود اوره 50 کیلوگرم از دسته کود شیمیایی. واحد فروش کیسه است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 3500000,
        "unit": "کیسه",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله 16 باغی /رول 400 متری",
        "slug": "KSH-P-00000023",
        "image": "",
        "blurb": "لوله 16 باغی /رول 400 متری. واحد فروش: رول.",
        "description": "لوله 16 باغی /رول 400 متری از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 5650000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله باغی / رول 200 متری",
        "slug": "KSH-P-00000024",
        "image": "",
        "blurb": "لوله 20 باغی / رول 200 متری. واحد فروش: رول.",
        "description": "لوله 20 باغی / رول 200 متری از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 4400000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 110",
        "slug": "KSH-P-00000044",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 110. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 110/ از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 528000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 125",
        "slug": "KSH-P-00000049",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 125. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 125 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 674000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 160",
        "slug": "KSH-P-00000053",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 160. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 160 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1112000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 200",
        "slug": "KSH-P-00000057",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 200. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 200 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1730000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 250",
        "slug": "KSH-P-00000061",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 250. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 250 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2700000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 315",
        "slug": "KSH-P-00000062",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 315. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 315 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1895000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 32",
        "slug": "KSH-P-00000026",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 32. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 32 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 47000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 50",
        "slug": "KSH-P-00000029",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 50. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 50 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 110000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 63",
        "slug": "KSH-P-00000031",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 63. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 63 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 176000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 75",
        "slug": "KSH-P-00000035",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 75. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 75 بار از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 250000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 90",
        "slug": "KSH-P-00000038",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 90. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 90 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 354000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله مه پاش/100 متر",
        "slug": "KSH-P-00000065",
        "image": "",
        "blurb": "لوله مه پاش/100 متر. واحد فروش: رول.",
        "description": "لوله مه پاش/100 متر از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1491000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "layflat",
        "name": "لوله نخدار/100 متر/1.5 بار",
        "slug": "KSH-P-00000004",
        "image": "/static/img/cat1.png",
        "blurb": "لوله نخدار /100 متر. واحد فروش: رول.",
        "description": "لوله نخدار /100 متر از دسته لوله نخدار. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 4368000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "layflat",
        "name": "لوله نخدار/100 متر/1.2 بار",
        "slug": "KSH-P-00000022",
        "image": "/static/img/cat1.png",
        "blurb": "لوله نخدار 1 اینچ/100 متر/1.2 بار. واحد فروش: رول.",
        "description": "لوله نخدار 1 اینچ/100 متر/1.2 بار از دسته لوله نخدار. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 11232000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ کشت دریپ",
        "slug": "KSH-P-00000002",
        "image": "/static/img/driptape.png",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2250000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "featured": True,
        "stock": 40,
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ خوشه چین",
        "slug": "KSH-P-00000001",
        "image": "/static/img/driptape.png",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2250000,
        "unit": "رول",
        "brand": "خوشه-چین",
        "badge": "",
        "featured": False,
        "stock": 40,
    },
]

SPECS = {
    "KSH-P-00000024": [
        {
            "working_pressure": "",
            "diameter": "25",
            "price": 6200000,
            "sort_order": 1,
        },
        {
            "working_pressure": "",
            "diameter": "20",
            "price": 4400000,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000044": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 238000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 520000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 528000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 640000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000049": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 306000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 520000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 550000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 674000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000053": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 492000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 744000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 914000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 1112000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000057": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 770000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 1168000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 1425000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 1730000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000061": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 1200000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 1805000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 2220000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 2700000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000062": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 1895000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 2850000,
            "sort_order": 0,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 3520000,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000026": [
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 40000,
            "sort_order": 0,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 47000,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000029": [
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 90000,
            "sort_order": 1,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 96000,
            "sort_order": 2,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 110000,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000031": [
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 150000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 140000,
            "sort_order": 0,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 176000,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000035": [
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 220000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 190000,
            "sort_order": 0,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 250000,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000038": [
        {
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 160000,
            "sort_order": 0,
        },
        {
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 270000,
            "sort_order": 0,
        },
        {
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 290000,
            "sort_order": 0,
        },
        {
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 354000,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000065": [
        {
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 1491000,
            "sort_order": 1,
        },
        {
            "working_pressure": "",
            "diameter": "1.5 اینچ",
            "price": 1581000,
            "sort_order": 2,
        },
        {
            "working_pressure": "",
            "diameter": "2 اینج",
            "price": 1809000,
            "sort_order": 3,
        },
        {
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 3300000,
            "sort_order": 4,
        },
    ],
    "KSH-P-00000004": [
        {
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 4368000,
            "sort_order": 1,
        },
        {
            "working_pressure": "",
            "diameter": "2 اینچ",
            "price": 5491000,
            "sort_order": 3,
        },
        {
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 6356000,
            "sort_order": 4,
        },
        {
            "working_pressure": "",
            "diameter": "3 اینچ",
            "price": 7737600,
            "sort_order": 5,
        },
        {
            "working_pressure": "",
            "diameter": "4 اینچ",
            "price": 9104000,
            "sort_order": 7,
        },
        {
            "working_pressure": "",
            "diameter": "5 اینچ",
            "price": 11980800,
            "sort_order": 8,
        },
        {
            "working_pressure": "",
            "diameter": "5.5 اینچ",
            "price": 13478400,
            "sort_order": 9,
        },
        {
            "working_pressure": "",
            "diameter": "6 اینچ",
            "price": 15724800,
            "sort_order": 10,
        },
        {
            "working_pressure": "",
            "diameter": "6.5 اینچ",
            "price": 18345600,
            "sort_order": 11,
        },
        {
            "working_pressure": "",
            "diameter": "8 اینچ",
            "price": 23337600,
            "sort_order": 12,
        },
    ],
    "KSH-P-00000022": [
        {
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 1123200,
            "sort_order": 1,
        },
        {
            "working_pressure": "",
            "diameter": "1.5 اینچ",
            "price": 3865000,
            "sort_order": 2,
        },
        {
            "working_pressure": "",
            "diameter": "2 اینچ",
            "price": 5000000,
            "sort_order": 3,
        },
        {
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 5865600,
            "sort_order": 4,
        },
        {
            "working_pressure": "",
            "diameter": "3 اینچ",
            "price": 7238400,
            "sort_order": 5,
        },
        {
            "working_pressure": "",
            "diameter": "4 اینچ",
            "price": 8236800,
            "sort_order": 6,
        },
        {
            "working_pressure": "",
            "diameter": "5 اینچ",
            "price": 11232000,
            "sort_order": 7,
        },
    ],
}


class Command(BaseCommand):
    help = "بارگذاری فهرست محصولات"

    def handle(self, *args, **options):
        self.stdout.write(self._current_database())
        Category.objects.all().delete()
        Brand.objects.all().delete()
        cats = {}
        brands = {}
        for row in CATEGORIES:
            cats[row["slug"]] = Category.objects.create(**row)
        for row in BRANDS:
            brands[row["slug"]] = Brand.objects.create(**row)
        for row in PRODUCTS:
            data = dict(row)
            category_slug = data.pop("category")
            brand_slug = data.pop("brand")
            featured = data.pop("featured", False)
            product = Product.objects.create(category=cats[category_slug], brand=brands[brand_slug], **data)
            for index, spec in enumerate(SPECS.get(product.slug, []), start=1):
                payload = dict(spec)
                payload.setdefault("slug", f"{product.slug}-{index}")
                if featured and index == 1:
                    payload["featured"] = True
                ProductVariant.objects.create(product=product, **payload)
        variant_count = sum(len(items) for items in SPECS.values())
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(cats)} دسته، {len(brands)} برند، {len(PRODUCTS)} محصول و {variant_count} تنوع ثبت شد."
            )
        )

    def _current_database(self):
        settings = connection.settings_dict
        engine = settings.get("ENGINE", "").rsplit(".", 1)[-1]
        name = settings.get("NAME") or ""
        host = settings.get("HOST") or ""
        port = settings.get("PORT") or ""
        user = settings.get("USER") or ""
        location = str(name)
        if host:
            location = f"{name} @ {host}:{port}" if port else f"{name} @ {host}"
        if user:
            location = f"{user}@{location}"
        counts = (
            f"{Category.objects.count()} دسته، "
            f"{Brand.objects.count()} برند، "
            f"{Product.objects.count()} محصول، "
            f"{ProductVariant.objects.count()} تنوع"
        )
        return f"پایگاه فعلی: {engine} ({location}) — {counts}"
