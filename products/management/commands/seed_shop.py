from django.core.management.base import BaseCommand
from django.db import connection

from products.models import Brand, Category, Product, ProductAttribute, ProductImage, ProductVariant

CATEGORIES = [
    {
        "name": "کود شیمیایی",
        "slug": "chemical-fertilizer",
        "tagline": "کود پایه برای تغذیه مزرعه و باغ",
        "image": "/static/img/categories/fert.webp",
        "showcase_image": "/static/img/showcase/fer-showcase.webp",
    },
    {
        "name": "تجهیزات",
        "slug": "equipment",
        "tagline": "لوله باغی، مه پاش",
        "image": "/static/img/categories/eqiup.webp",
        "showcase_image": "/static/img/showcase/eqiup-showcase.webp",
    },
    {
        "name": "لوله پلی اتیلن",
        "slug": "pe-pipe",
        "tagline": "لوله پلی‌اتیلن در سایز و فشار کاری مختلف، فروش متری.",
        "image": "/static/img/categories/poly.webp",
        "showcase_image": "",
    },
    {
        "name": "لوله نخدار",
        "slug": "layflat",
        "tagline": "لوله نخدار در سایزهای اینچی، رول صد متری.",
        "image": "/static/img/categories/nakh.webp",
        "showcase_image": "",
    },
    {
        "name": "نوار تیپ",
        "slug": "drip-tape",
        "tagline": "نوار تیپ آبیاری قطره ای طول 1000 متر",
        "image": "/static/img/categories/drip.webp",
        "showcase_image": "/static/img/showcase/drip-showcase.webp",
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
        "image": "",
        "blurb": "کود اوره 50 کیلوگرم. واحد فروش: کیسه.",
        "description": "کود اوره 50 کیلوگرم از دسته کود شیمیایی. واحد فروش کیسه است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 3500000,
        "unit": "کیسه",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله 16 باغی /رول 400 متری",
        "slug": "KSH-P-00000023",
        "image": "/static/img/baghi.webp",
        "blurb": "لوله 16 باغی /رول 400 متری. واحد فروش: رول.",
        "description": "لوله 16 باغی /رول 400 متری از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 5650000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله باغی / رول 200 متری",
        "slug": "KSH-P-00000024",
        "image": "/static/img/baghi.webp",
        "blurb": "لوله 20 باغی / رول 200 متری. واحد فروش: رول.",
        "description": "لوله 20 باغی / رول 200 متری از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 4400000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
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
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 32",
        "slug": "KSH-P-00000026",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 32. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 32 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 47000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 50",
        "slug": "KSH-P-00000029",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 50. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 50 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 110000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 63",
        "slug": "KSH-P-00000031",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 63. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 63 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 176000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
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
        "stock": 40,
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 90",
        "slug": "KSH-P-00000038",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 90. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 90 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 354000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "equipment",
        "name": "لوله مه پاش/100 متر",
        "slug": "KSH-P-00000065",
        "image": "/static/img/meh.webp",
        "blurb": "لوله مه پاش/100 متر. واحد فروش: رول.",
        "description": "لوله مه پاش/100 متر از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1491000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "پرفروش",
        "stock": 40,
    },
    {
        "category": "layflat",
        "name": "لوله نخدار/100 متر/1.5 بار",
        "slug": "KSH-P-00000004",
        "image": "/static/img/nakh.webp",
        "blurb": "لوله نخدار /100 متر. واحد فروش: رول.",
        "description": "لوله نخدار /100 متر از دسته لوله نخدار. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 4368000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "layflat",
        "name": "لوله نخدار/100 متر/1.2 بار",
        "slug": "KSH-P-00000022",
        "image": "/static/img/nakh.webp",
        "blurb": "لوله نخدار 1 اینچ/100 متر/1.2 بار. واحد فروش: رول.",
        "description": "لوله نخدار 1 اینچ/100 متر/1.2 بار از دسته لوله نخدار. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 11232000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
        "stock": 40,
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ کشت دریپ",
        "slug": "KSH-P-00000002",
        "image": "/static/img/driptape3.webp",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ 1000 متری دوخت بغل برند کشت دریپ. \r\nدر دو اندازه ی 10 سانت و 20 سانت.\r\nتولید شده با مواد اولیه درجه یک مواد نو.\r\nداری تضمین یک مرتبه کشت.\r\nفشار کاری 0.6 تا 1 بار.\r\nقطر داخلی 16 میلی متر.\r\nضخامت 175 میکرون. \r\nوزن هر رول حدودا 10 کیلوگرم.",
        "price": 2250000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "پرفروش",
        "stock": 40,
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ خوشه چین",
        "slug": "KSH-P-00000001",
        "image": "/static/img/khooshe.webp",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ 1000 متری دوخت بغل برند خوشه چین. \r\nدر دو اندازه ی 10 سانت و 20 سانت.\r\nتولید شده با مواد اولیه درجه یک مواد نو.\r\nداری تضمین یک مرتبه کشت.\r\nفشار کاری 0.6 تا 1 بار.\r\nقطر داخلی 16 میلی متر.\r\nضخامت 175 میکرون. \r\nوزن هر رول حدودا 10 کیلوگرم.",
        "price": 2250000,
        "unit": "رول",
        "brand": "خوشه-چین",
        "badge": "پرفروش",
        "stock": 40,
    },
]

SPECS = {
    "KSH-P-00000024": [
        {
            "slug": "KSH-P-00000024-70",
            "working_pressure": "",
            "diameter": "25",
            "price": 6200000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000024-71",
            "working_pressure": "",
            "diameter": "20",
            "price": 4400000,
            "featured": True,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000044": [
        {
            "slug": "KSH-P-00000044-72",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 238000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000044-73",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 520000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000044-74",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 528000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000044-75",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 640000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000049": [
        {
            "slug": "KSH-P-00000049-76",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 306000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000049-77",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 520000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000049-78",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 550000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000049-79",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 674000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000053": [
        {
            "slug": "KSH-P-00000053-80",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 492000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000053-81",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 744000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000053-82",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 914000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000053-83",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 1112000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000057": [
        {
            "slug": "KSH-P-00000057-84",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 770000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000057-85",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 1168000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000057-86",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 1425000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000057-87",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 1730000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000061": [
        {
            "slug": "KSH-P-00000061-88",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 1200000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000061-89",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 1805000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000061-90",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 2220000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000061-91",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 2700000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000062": [
        {
            "slug": "KSH-P-00000062-92",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 1895000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000062-93",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 2850000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000062-94",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 3520000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000026": [
        {
            "slug": "KSH-P-00000026-95",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 40000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000026-96",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 47000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000029": [
        {
            "slug": "KSH-P-00000029-97",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 90000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000029-98",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 96000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000029-99",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 110000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000031": [
        {
            "slug": "KSH-P-00000031-100",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 150000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000031-101",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 140000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000031-102",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 176000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000035": [
        {
            "slug": "KSH-P-00000035-103",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 220000,
            "featured": True,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000035-104",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 190000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000035-105",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 250000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000038": [
        {
            "slug": "KSH-P-00000038-106",
            "working_pressure": "4 بار",
            "diameter": "",
            "price": 160000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000038-107",
            "working_pressure": "6 بار",
            "diameter": "",
            "price": 270000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000038-108",
            "working_pressure": "8 بار",
            "diameter": "",
            "price": 290000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000038-109",
            "working_pressure": "10 بار",
            "diameter": "",
            "price": 354000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000065": [
        {
            "slug": "KSH-P-00000065-110",
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 1491000,
            "featured": True,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000065-111",
            "working_pressure": "",
            "diameter": "1.5 اینچ",
            "price": 1581000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000065-112",
            "working_pressure": "",
            "diameter": "2 اینج",
            "price": 1809000,
            "featured": True,
            "sort_order": 3,
        },
        {
            "slug": "KSH-P-00000065-113",
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 3300000,
            "featured": False,
            "sort_order": 4,
        },
    ],
    "KSH-P-00000004": [
        {
            "slug": "KSH-P-00000004-114",
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 4368000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000004-115",
            "working_pressure": "",
            "diameter": "2 اینچ",
            "price": 5491000,
            "featured": False,
            "sort_order": 3,
        },
        {
            "slug": "KSH-P-00000004-116",
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 6356000,
            "featured": False,
            "sort_order": 4,
        },
        {
            "slug": "KSH-P-00000004-117",
            "working_pressure": "",
            "diameter": "3 اینچ",
            "price": 7737600,
            "featured": False,
            "sort_order": 5,
        },
        {
            "slug": "KSH-P-00000004-118",
            "working_pressure": "",
            "diameter": "4 اینچ",
            "price": 9104000,
            "featured": False,
            "sort_order": 7,
        },
        {
            "slug": "KSH-P-00000004-119",
            "working_pressure": "",
            "diameter": "5 اینچ",
            "price": 11980800,
            "featured": False,
            "sort_order": 8,
        },
        {
            "slug": "KSH-P-00000004-120",
            "working_pressure": "",
            "diameter": "5.5 اینچ",
            "price": 13478400,
            "featured": False,
            "sort_order": 9,
        },
        {
            "slug": "KSH-P-00000004-121",
            "working_pressure": "",
            "diameter": "6 اینچ",
            "price": 15724800,
            "featured": False,
            "sort_order": 10,
        },
        {
            "slug": "KSH-P-00000004-122",
            "working_pressure": "",
            "diameter": "6.5 اینچ",
            "price": 18345600,
            "featured": True,
            "sort_order": 11,
        },
        {
            "slug": "KSH-P-00000004-123",
            "working_pressure": "",
            "diameter": "8 اینچ",
            "price": 23337600,
            "featured": False,
            "sort_order": 12,
        },
    ],
    "KSH-P-00000022": [
        {
            "slug": "KSH-P-00000022-124",
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 1123200,
            "featured": True,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000022-125",
            "working_pressure": "",
            "diameter": "1.5 اینچ",
            "price": 3865000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000022-126",
            "working_pressure": "",
            "diameter": "2 اینچ",
            "price": 5000000,
            "featured": False,
            "sort_order": 3,
        },
        {
            "slug": "KSH-P-00000022-127",
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 5865600,
            "featured": False,
            "sort_order": 4,
        },
        {
            "slug": "KSH-P-00000022-128",
            "working_pressure": "",
            "diameter": "3 اینچ",
            "price": 7238400,
            "featured": False,
            "sort_order": 5,
        },
        {
            "slug": "KSH-P-00000022-129",
            "working_pressure": "",
            "diameter": "4 اینچ",
            "price": 8236800,
            "featured": False,
            "sort_order": 6,
        },
        {
            "slug": "KSH-P-00000022-130",
            "working_pressure": "",
            "diameter": "5 اینچ",
            "price": 11232000,
            "featured": False,
            "sort_order": 7,
        },
    ],
}

ATTRIBUTES = {
    "KSH-P-00000002": [
        {
            "name": "قطر",
            "value": "16 میلی متر",
            "sort_order": 0,
        },
        {
            "name": "فاصله",
            "value": "20 سانت و 10 سانت",
            "sort_order": 0,
        },
    ],
    "KSH-P-00000001": [
        {
            "name": "قطر",
            "value": "16 میلی متر",
            "sort_order": 0,
        },
        {
            "name": "فاصله",
            "value": "20 سانت و 10 سانت",
            "sort_order": 0,
        },
    ],
}

IMAGES = {
    "KSH-P-00000004": [
        {
            "image": "/static/img/nakh.webp",
            "alt": "نخدار",
            "sort_order": 0,
        },
    ],
    "KSH-P-00000022": [
        {
            "image": "/static/img/nakh.webp",
            "alt": "نخدار",
            "sort_order": 0,
        },
    ],
    "KSH-P-00000002": [
        {
            "image": "/static/img/driptape3.webp",
            "alt": "نوارتیپ3",
            "sort_order": 0,
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
            product = Product.objects.create(category=cats[category_slug], brand=brands[brand_slug], **data)
            for spec in SPECS.get(product.slug, []):
                ProductVariant.objects.create(product=product, **spec)
            for attr in ATTRIBUTES.get(product.slug, []):
                ProductAttribute.objects.create(product=product, **attr)
            for image in IMAGES.get(product.slug, []):
                ProductImage.objects.create(product=product, **image)
        variant_count = sum(len(items) for items in SPECS.values())
        attribute_count = sum(len(items) for items in ATTRIBUTES.values())
        image_count = sum(len(items) for items in IMAGES.values())
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(cats)} دسته، {len(brands)} برند، {len(PRODUCTS)} محصول، "
                f"{variant_count} تنوع، {attribute_count} ویژگی و {image_count} تصویر ثبت شد."
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
            f"{ProductVariant.objects.count()} تنوع، "
            f"{ProductAttribute.objects.count()} ویژگی، "
            f"{ProductImage.objects.count()} تصویر"
        )
        return f"پایگاه فعلی: {engine} ({location}) — {counts}"
