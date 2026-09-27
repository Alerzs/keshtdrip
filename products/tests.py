from django.test import TestCase
from django.urls import reverse

from products.models import Brand, Category, Product, ProductVariant


class ProductVariantTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="آبیاری تست", slug="variant-irrigation", tagline="آب")
        brand = Brand.objects.create(name="برند تست", slug="variant-brand")
        self.product = Product.objects.create(
            category=category,
            brand=brand,
            name="لوله قطره‌ای",
            slug="drip-pipe",
            blurb="لوله",
            description="توضیح",
            price=1000,
            unit="متر",
        )
        self.low = ProductVariant.objects.create(
            product=self.product,
            working_pressure="2 بار",
            diameter="16 میلی‌متر",
            price=100000,
        )
        self.high = ProductVariant.objects.create(
            product=self.product,
            working_pressure="4 بار",
            diameter="20 میلی‌متر",
            price=180000,
        )
        self.plain = Product.objects.create(
            category=category,
            brand=brand,
            name="کوزه",
            slug="olla",
            blurb="کوزه",
            description="توضیح",
            price=640000,
            unit="جفت",
        )

    def test_catalog_shows_each_pressure_and_diameter_as_its_own_box(self):
        response = self.client.get(reverse("catalog"))
        self.assertContains(response, "لوله قطره‌ای", count=3)
        self.assertContains(response, "۱۰۰٬۰۰۰")
        self.assertContains(response, "۱۸۰٬۰۰۰")
        self.assertContains(response, "کوزه", count=2)

    def test_product_page_prices_the_selected_combination(self):
        response = self.client.get(self.high.get_absolute_url())
        self.assertContains(response, "۱۸۰٬۰۰۰")
        self.assertContains(response, 'name="working_pressure"')
        self.assertContains(response, 'name="diameter"')
        self.assertContains(response, "4 بار")
        self.assertContains(response, "20 میلی‌متر")

    def test_cart_uses_the_chosen_combination_price(self):
        self.client.post(
            reverse("add_to_cart", args=[self.product.slug]),
            {"quantity": 2, "working_pressure": "4 بار", "diameter": "20 میلی‌متر"},
        )
        self.client.post(
            reverse("add_to_cart", args=[self.product.slug]),
            {"quantity": 1, "working_pressure": "2 بار", "diameter": "16 میلی‌متر"},
        )
        response = self.client.get(reverse("cart"))
        self.assertContains(response, "قطر ۲۰ میلی‌متر، فشار کاری ۴ بار")
        self.assertContains(response, "قطر ۱۶ میلی‌متر، فشار کاری ۲ بار")
        self.assertContains(response, "۳۶۰٬۰۰۰")
        self.assertContains(response, "۴۶۰٬۰۰۰")

    def test_unknown_combination_is_rejected(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.product.slug]),
            {"quantity": 1, "working_pressure": "2 بار", "diameter": "20 میلی‌متر"},
        )
        self.assertRedirects(response, self.product.get_absolute_url())
        cart = self.client.get(reverse("cart"))
        self.assertContains(cart, "سبد خرید")
        self.assertNotContains(cart, "لوله قطره‌ای")


class SeoTests(TestCase):
    def test_home_targets_tape_and_irrigation_keywords(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "خرید نوار تیپ و لوازم آبیاری | کشت‌دریپ")
        self.assertContains(response, "خرید نوار تیپ پلاکدار و درزدار")
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, "application/ld+json")
        self.assertContains(response, "OnlineStore")
        html = response.content.decode()
        self.assertEqual(html.count("<h1"), 1)

    def test_drip_tape_catalog_title_and_heading(self):
        Category.objects.create(name="نوار تیپ", slug="drip-tape", tagline="نوار تیپ آبیاری")
        response = self.client.get(reverse("catalog") + "?category=drip-tape")
        self.assertContains(response, "خرید نوار تیپ | کشت‌دریپ")
        self.assertContains(response, "<h1")
        self.assertContains(response, "خرید نوار تیپ")
        self.assertContains(response, "index, follow")

    def test_shop_and_search_robots(self):
        shop = self.client.get(reverse("catalog"))
        self.assertContains(shop, "خرید لوازم آبیاری | کشت‌دریپ")
        search = self.client.get(reverse("catalog") + "?q=نوار")
        self.assertContains(search, "noindex, follow")
        cart = self.client.get(reverse("cart"))
        self.assertContains(cart, "noindex, follow")

    def test_robots_and_sitemap(self):
        category = Category.objects.create(name="نوار تیپ", slug="drip-tape", tagline="نوار")
        brand = Brand.objects.create(name="کشت‌دریپ", slug="seo-brand")
        Product.objects.create(
            category=category,
            brand=brand,
            name="نوار تیپ نمونه",
            slug="seo-tape",
            blurb="نوار تیپ",
            description="توضیح",
            price=1000,
            unit="رول",
        )
        robots = self.client.get(reverse("robots"))
        self.assertContains(robots, "Sitemap:")
        self.assertContains(robots, "Disallow: /basket/")
        sitemap = self.client.get(reverse("sitemap"))
        self.assertContains(sitemap, "category=drip-tape")
        self.assertContains(sitemap, "/product/seo-tape/")
        self.assertContains(sitemap, "/blog/how-to-choose-drip-tape/")

    def test_product_schema_uses_rial(self):
        category = Category.objects.create(name="نوار تیپ", slug="seo-tape-cat", tagline="نوار")
        brand = Brand.objects.create(name="کشت‌دریپ", slug="seo-brand-2")
        product = Product.objects.create(
            category=category,
            brand=brand,
            name="نوار تیپ تست",
            slug="seo-tape-product",
            blurb="نوار تیپ برای آبیاری",
            description="توضیح",
            price=250000,
            unit="رول",
        )
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, "خرید نوار تیپ تست | کشت‌دریپ")
        self.assertContains(response, '"priceCurrency": "IRR"')
        self.assertContains(response, '"price": 2500000')
