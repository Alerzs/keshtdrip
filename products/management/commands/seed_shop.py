from django.core.management.base import BaseCommand
from django.db import connection

from products.models import Brand, Category, Product, ProductAttribute, ProductImage

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
        "image": "/static/img/fertelizer.webp",
        "blurb": "کود اوره 50 کیلوگرم. واحد فروش: کیسه.",
        "description": "کود اوره 50 کیلوگرم از دسته کود شیمیایی. واحد فروش کیسه است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 3500000,
        "unit": "کیسه",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "equipment",
        "name": "لوله باغی / رول 400 متر",
        "slug": "KSH-P-00000023",
        "image": "/static/img/baghi.webp",
        "blurb": "لوله باغی / رول 400 متر. واحد فروش: رول.",
        "description": "لوله باغی / رول 400 متر از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 5650000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "equipment",
        "name": "لوله باغی / رول 200 متر",
        "slug": "KSH-P-00000024",
        "image": "/static/img/baghi.webp",
        "blurb": "لوله باغی / رول 200 متر. واحد فروش: رول.",
        "description": "لوله باغی / رول 200 متر از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 4400000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 110",
        "slug": "KSH-P-00000044",
        "image": "/static/img/pe-110.webp",
        "blurb": "لوله پلی اتیلن سایز 110. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 110 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 610500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 125",
        "slug": "KSH-P-00000049",
        "image": "/static/img/pe-125.webp",
        "blurb": "لوله پلی اتیلن سایز 125. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 125 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 779500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 160",
        "slug": "KSH-P-00000053",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 160. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 160 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 1286000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 200",
        "slug": "KSH-P-00000057",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 200. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 200 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2312000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 250",
        "slug": "KSH-P-00000061",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 250. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 250 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 3122000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 315",
        "slug": "KSH-P-00000062",
        "image": "",
        "blurb": "لوله پلی اتیلن سایز 315. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 315 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2190000,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 32",
        "slug": "KSH-P-00000026",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 32. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 32 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 54500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 50",
        "slug": "KSH-P-00000029",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 50. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 50 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 127500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 63",
        "slug": "KSH-P-00000031",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 63. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 63 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 203500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 75",
        "slug": "KSH-P-00000035",
        "image": "/static/img/pe-75.webp",
        "blurb": "لوله پلی اتیلن سایز 75. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 75 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 289500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "pe-pipe",
        "name": "لوله پلی اتیلن سایز 90",
        "slug": "KSH-P-00000038",
        "image": "/static/img/pipe.webp",
        "blurb": "لوله پلی اتیلن سایز 90. واحد فروش: متر.",
        "description": "لوله پلی اتیلن سایز 90 از دسته لوله پلی اتیلن. واحد فروش متر است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 409500,
        "unit": "متر",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "equipment",
        "name": "لوله مه پاش / 100 متر",
        "slug": "KSH-P-00000065",
        "image": "/static/img/meh.webp",
        "blurb": "لوله مه پاش / 100 متر. واحد فروش: رول.",
        "description": "لوله مه پاش / 100 متر از دسته تجهیزات. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 2000000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "پرفروش",
    },
    {
        "category": "layflat",
        "name": "لوله نخدار / 100 متر",
        "slug": "KSH-P-00000004",
        "image": "/static/img/nakh.webp",
        "blurb": "لوله نخدار / 100 متر. واحد فروش: رول.",
        "description": "لوله نخدار / 100 متر از دسته لوله نخدار. واحد فروش رول است و قیمت درج‌شده قیمت فروش به تومان است.",
        "price": 5625000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "",
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ کشت دریپ",
        "slug": "KSH-P-00000002",
        "image": "/static/img/driptape3.webp",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ 1000 متری دوخت بغل برند کشت دریپ. \r\nدر دو اندازه ی 10 سانت و 20 سانت.\r\nتولید شده با مواد اولیه درجه یک مواد نو.\r\nداری تضمین یک مرتبه کشت.\r\nفشار کاری 0.6 تا 1 بار.\r\nقطر داخلی 16 میلی متر.\r\nضخامت 175 میکرون. \r\nوزن هر رول حدودا 10 کیلوگرم.",
        "price": 2350000,
        "unit": "رول",
        "brand": "keshtdrip",
        "badge": "پرفروش",
    },
    {
        "category": "drip-tape",
        "name": "نوار تیپ خوشه چین",
        "slug": "KSH-P-00000001",
        "image": "/static/img/khooshe.webp",
        "blurb": "نوار تیپ. واحد فروش: رول.",
        "description": "نوار تیپ 1000 متری دوخت بغل برند خوشه چین. \r\nدر دو اندازه ی 10 سانت و 20 سانت.\r\nتولید شده با مواد اولیه درجه یک مواد نو.\r\nداری تضمین یک مرتبه کشت.\r\nفشار کاری 0.6 تا 1 بار.\r\nقطر داخلی 16 میلی متر.\r\nضخامت 175 میکرون. \r\nوزن هر رول حدودا 10 کیلوگرم.",
        "price": 2350000,
        "unit": "رول",
        "brand": "خوشه-چین",
        "badge": "پرفروش",
    },
]

# Each spec becomes its own product. Codes, prices, pressure, and diameter
# follow the Keshtyar price list dated 2026-11-15.
SPECS = {
    "KSH-P-00000023": [
        {
            "slug": "KSH-P-00000023",
            "working_pressure": "",
            "diameter": "16 میل",
            "price": 5650000,
            "featured": False,
            "sort_order": 0,
        },
    ],
    "KSH-P-00000024": [
        {
            "slug": "KSH-P-00000024",
            "working_pressure": "",
            "diameter": "20 میل",
            "price": 4400000,
            "featured": True,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000069",
            "working_pressure": "",
            "diameter": "25 میل",
            "price": 6200000,
            "featured": False,
            "sort_order": 1,
        },
    ],
    "KSH-P-00000044": [
        {
            "slug": "KSH-P-00000041",
            "working_pressure": "4 بار",
            "diameter": "4 اینچ",
            "price": 275500,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000042",
            "working_pressure": "6 بار",
            "diameter": "4 اینچ",
            "price": 462500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000043",
            "working_pressure": "8 بار",
            "diameter": "4 اینچ",
            "price": 509000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000044",
            "working_pressure": "10 بار",
            "diameter": "4 اینچ",
            "price": 610500,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000049": [
        {
            "slug": "KSH-P-00000045",
            "working_pressure": "4 بار",
            "diameter": "5 اینچ",
            "price": 354000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000047",
            "working_pressure": "6 بار",
            "diameter": "5 اینچ",
            "price": 601500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000048",
            "working_pressure": "8 بار",
            "diameter": "5 اینچ",
            "price": 636000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000049",
            "working_pressure": "10 بار",
            "diameter": "5 اینچ",
            "price": 779500,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000053": [
        {
            "slug": "KSH-P-00000050",
            "working_pressure": "4 بار",
            "diameter": "6 اینچ",
            "price": 567000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000051",
            "working_pressure": "6 بار",
            "diameter": "6 اینچ",
            "price": 860500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000052",
            "working_pressure": "8 بار",
            "diameter": "6 اینچ",
            "price": 1057000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000053",
            "working_pressure": "10 بار",
            "diameter": "6 اینچ",
            "price": 1286000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000057": [
        {
            "slug": "KSH-P-00000054",
            "working_pressure": "4 بار",
            "diameter": "8 اینچ",
            "price": 888000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000055",
            "working_pressure": "6 بار",
            "diameter": "8 اینچ",
            "price": 1350500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000056",
            "working_pressure": "8 بار",
            "diameter": "8 اینچ",
            "price": 1646500,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000057",
            "working_pressure": "10 بار",
            "diameter": "8 اینچ",
            "price": 2312000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000061": [
        {
            "slug": "KSH-P-00000058",
            "working_pressure": "4 بار",
            "diameter": "10 اینچ",
            "price": 1383000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000059",
            "working_pressure": "6 بار",
            "diameter": "10 اینچ",
            "price": 2086000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000060",
            "working_pressure": "8 بار",
            "diameter": "10 اینچ",
            "price": 2567000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000061",
            "working_pressure": "10 بار",
            "diameter": "10 اینچ",
            "price": 3122000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000062": [
        {
            "slug": "KSH-P-00000062",
            "working_pressure": "4 بار",
            "diameter": "12 اینچ",
            "price": 2190000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000063",
            "working_pressure": "6 بار",
            "diameter": "12 اینچ",
            "price": 3307000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000064",
            "working_pressure": "8 بار",
            "diameter": "12 اینچ",
            "price": 4070000,
            "featured": False,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000026": [
        {
            "slug": "KSH-P-00000025",
            "working_pressure": "8 بار",
            "diameter": "1 اینچ",
            "price": 46000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000026",
            "working_pressure": "10 بار",
            "diameter": "1 اینچ",
            "price": 54500,
            "featured": False,
            "sort_order": 1,
        },
    ],
    "KSH-P-00000029": [
        {
            "slug": "KSH-P-00000027",
            "working_pressure": "6 بار",
            "diameter": "1.5 اینچ",
            "price": 104500,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000028",
            "working_pressure": "8 بار",
            "diameter": "1.5 اینچ",
            "price": 111000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000029",
            "working_pressure": "10 بار",
            "diameter": "1.5 اینچ",
            "price": 127500,
            "featured": False,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000031": [
        {
            "slug": "KSH-P-00000030",
            "working_pressure": "6 بار",
            "diameter": "2 اینچ",
            "price": 162000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000032",
            "working_pressure": "8 بار",
            "diameter": "2 اینچ",
            "price": 173500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000031",
            "working_pressure": "10 بار",
            "diameter": "2 اینچ",
            "price": 203500,
            "featured": False,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000035": [
        {
            "slug": "KSH-P-00000033",
            "working_pressure": "6 بار",
            "diameter": "2.5 اینچ",
            "price": 220000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000034",
            "working_pressure": "8 بار",
            "diameter": "2.5 اینچ",
            "price": 241000,
            "featured": True,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000035",
            "working_pressure": "10 بار",
            "diameter": "2.5 اینچ",
            "price": 289500,
            "featured": False,
            "sort_order": 2,
        },
    ],
    "KSH-P-00000038": [
        {
            "slug": "KSH-P-00000036",
            "working_pressure": "4 بار",
            "diameter": "3 اینچ",
            "price": 185000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000037",
            "working_pressure": "6 بار",
            "diameter": "3 اینچ",
            "price": 312500,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000040",
            "working_pressure": "8 بار",
            "diameter": "3 اینچ",
            "price": 355500,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000038",
            "working_pressure": "10 بار",
            "diameter": "3 اینچ",
            "price": 409500,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000065": [
        {
            "slug": "KSH-P-00000065",
            "working_pressure": "",
            "diameter": "1 اینچ",
            "price": 2000000,
            "featured": True,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000066",
            "working_pressure": "",
            "diameter": "1.5 اینچ",
            "price": 2438000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000067",
            "working_pressure": "",
            "diameter": "2 اینچ",
            "price": 2725000,
            "featured": True,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000068",
            "working_pressure": "",
            "diameter": "2.5 اینچ",
            "price": 5063000,
            "featured": False,
            "sort_order": 3,
        },
    ],
    "KSH-P-00000004": [
        {
            "slug": "KSH-P-00000004",
            "working_pressure": "1.5 بار",
            "diameter": "2 اینچ",
            "price": 5625000,
            "featured": False,
            "sort_order": 0,
        },
        {
            "slug": "KSH-P-00000005",
            "working_pressure": "1.5 بار",
            "diameter": "2.5 اینچ",
            "price": 7188000,
            "featured": False,
            "sort_order": 1,
        },
        {
            "slug": "KSH-P-00000006",
            "working_pressure": "1.5 بار",
            "diameter": "3 اینچ",
            "price": 8375000,
            "featured": False,
            "sort_order": 2,
        },
        {
            "slug": "KSH-P-00000007",
            "working_pressure": "1.5 بار",
            "diameter": "3.5 اینچ",
            "price": 10063000,
            "featured": False,
            "sort_order": 3,
        },
        {
            "slug": "KSH-P-00000008",
            "working_pressure": "1.5 بار",
            "diameter": "4 اینچ",
            "price": 11938000,
            "featured": False,
            "sort_order": 4,
        },
        {
            "slug": "KSH-P-00000009",
            "working_pressure": "1.5 بار",
            "diameter": "4.5 اینچ",
            "price": 13063000,
            "featured": False,
            "sort_order": 5,
        },
        {
            "slug": "KSH-P-00000010",
            "working_pressure": "1.5 بار",
            "diameter": "5 اینچ",
            "price": 15688000,
            "featured": False,
            "sort_order": 6,
        },
        {
            "slug": "KSH-P-00000012",
            "working_pressure": "1.5 بار",
            "diameter": "6 اینچ",
            "price": 20563000,
            "featured": False,
            "sort_order": 7,
        },
        {
            "slug": "KSH-P-00000014",
            "working_pressure": "1.5 بار",
            "diameter": "6.5 اینچ",
            "price": 23813000,
            "featured": True,
            "sort_order": 8,
        },
        {
            "slug": "KSH-P-00000015",
            "working_pressure": "1.5 بار",
            "diameter": "8 اینچ",
            "price": 30375000,
            "featured": False,
            "sort_order": 9,
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
    "KSH-P-00000002": [
        {
            "image": "/static/img/driptape3.webp",
            "alt": "نوارتیپ3",
            "sort_order": 0,
        },
    ],
}


def _spec_attributes(spec, extra):
    attributes = []
    order = 0
    if spec.get("diameter"):
        attributes.append({"name": "قطر", "value": spec["diameter"], "sort_order": order})
        order += 1
    if spec.get("working_pressure"):
        attributes.append({"name": "فشار کاری", "value": spec["working_pressure"], "sort_order": order})
        order += 1
    for attr in extra:
        attributes.append({**attr, "sort_order": order})
        order += 1
    return attributes


def _spec_name(name, spec):
    parts = []
    if spec.get("diameter"):
        parts.append(f"قطر {spec['diameter']}")
    if spec.get("working_pressure"):
        parts.append(f"فشار کاری {spec['working_pressure']}")
    if not parts:
        return name
    return f"{name} — {'، '.join(parts)}"[:140]


def expanded_products():
    rows = []
    for row in PRODUCTS:
        specs = SPECS.get(row["slug"], [])
        base_attributes = list(ATTRIBUTES.get(row["slug"], []))
        images = list(IMAGES.get(row["slug"], []))
        if not specs:
            data = dict(row)
            data["featured"] = False
            data["attributes"] = base_attributes
            data["images"] = images
            rows.append(data)
            continue
        for spec in specs:
            data = dict(row)
            data["slug"] = spec["slug"]
            data["price"] = spec["price"]
            data["featured"] = bool(spec.get("featured"))
            data["name"] = _spec_name(row["name"], spec)
            data["attributes"] = _spec_attributes(spec, base_attributes)
            data["images"] = images
            rows.append(data)
    return rows


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
        products = expanded_products()
        for row in products:
            data = dict(row)
            category_slug = data.pop("category")
            brand_slug = data.pop("brand")
            attributes = data.pop("attributes")
            images = data.pop("images")
            product = Product.objects.create(category=cats[category_slug], brand=brands[brand_slug], **data)
            for attr in attributes:
                ProductAttribute.objects.create(product=product, **attr)
            for image in images:
                ProductImage.objects.create(product=product, **image)
        attribute_count = sum(len(item["attributes"]) for item in products)
        image_count = sum(len(item["images"]) for item in products)
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(cats)} دسته، {len(brands)} برند، {len(products)} محصول، "
                f"{attribute_count} ویژگی و {image_count} تصویر ثبت شد."
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
            f"{ProductAttribute.objects.count()} ویژگی، "
            f"{ProductImage.objects.count()} تصویر"
        )
        return f"پایگاه فعلی: {engine} ({location}) — {counts}"
