"""A module that sets up the environment for testing the app's pages"""
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from front.models import (
    SocialMedia, PhoneCategory, PhoneMemorySize,
    Currency, ItemIcon, CountryCode, User,
    Order, OrderStatus, PaymentMethod, ShippingAddress,
    NewsItem, cache, Cart, PhoneBrand, PhoneModel,
    PhoneModelList, Color
    )


class BaseSeleniumTestCase(StaticLiveServerTestCase):
    """Provides tools for testing the pages."""
    def setUp(self):
        """Setup initial test environment."""
        super(BaseSeleniumTestCase, self).setUp()

    def create_social_media(self):
        """Create social media links."""
        SocialMedia.objects.create(
            url_link="https://facebook.com", icon="fa fa-facebook",
            name="Facebook"
            )
        SocialMedia.objects.create(
            url_link="https://instagram.com", icon="fa fa-instagram",
            name="Instagram"
            )

    def create_phone_category(self):
        """Create phone categories."""
        PhoneCategory.objects.create(
            phone_category="iPhone",
            category_image="phone_categories/test_image_6.png"
            )
        self.iphone = PhoneCategory.objects.get(phone_category="iPhone")
        PhoneCategory.objects.create(
            phone_category="Android",
            category_image="phone_categories/test_image_6.png"
            )
        self.android = PhoneCategory.objects.get(phone_category="Android")

    def create_phone_memory_size(self):
        """Add phone memory sizes."""
        PhoneMemorySize.objects.create(
            abbreviation="GB", size_number=8, category=self.iphone
            )
        self.iphone_size = PhoneMemorySize.objects.get(category=self.iphone)
        PhoneMemorySize.objects.create(
            abbreviation="GB", size_number=16, category=self.android
            )
        self.android_size = PhoneMemorySize.objects.get(category=self.iphone)

    def create_currency(self):
        """Create currency."""
        Currency.objects.create(
            currency_abbreviation="Kshs.",
            currency_long_form="Kenya Shillings"
            )
        self.currency = Currency.objects.get(currency_abbreviation="Kshs.")

    def create_item_icon(self):
        """Create phone icons."""
        ItemIcon.objects.create(item_icon="iphone")
        self.iphone_icon = ItemIcon.objects.get(item_icon="iphone")
        ItemIcon.objects.create(item_icon="android")
        self.android_icon = ItemIcon.objects.get(item_icon="android")

    def create_country_code(self):
        """Create country codes."""
        CountryCode.objects.create(country_code=254, country="Kenya")
        self.country_code = CountryCode.objects.get(country="Kenya")

    def create_user(self):
        """Create test user."""
        User.objects.create(
            email="timonpumba@gmail.com", first_name="timon",
            last_name="pumba", is_staff=True, is_active=True,
            is_change_allowed=False,
            country_code=self.country_code,
            phone_number=722000000
            )
        self.timon = User.objects.get(email="timonpumba@gmail.com")
        self.timon.set_password("secret")
        self.timon.save()

    def create_order_status(self):
        """Create default order status"""
        OrderStatus.objects.create(status="pending")
        self.order_status = OrderStatus.objects.get(status="pending")

    def create_payment_method(self):
        """Create payment method."""
        PaymentMethod.objects.create(payment_method="Mpesa")
        self.mpesa = PaymentMethod.objects.get(payment_method="Mpesa")

    def create_order(self):
        """Create an order"""
        Cart.objects.create(owner=None)
        cart = Cart.objects.get(owner=None)
        Order.objects.create(
            owner=self.timon, phone=self.iphone_6_s_rose_gold,
            status=self.order_status, quantity=2,
            price=10000, total_price=20000,
            payment_method=self.mpesa, date="2018-12-12",
            cart=cart
            )
        self.order = Order.objects.get(owner=self.timon)

    def create_shipping_address(self):
        """Create a shipping address."""
        ShippingAddress.objects.create(
            order=self.order, pickup="Evergreen Center",
            location="Kiambu Road", recepient="Nala"
            )

    def create_news(self):
        """Create a news link"""
        NewsItem.objects.create(
            title="Teke rocks", source="Medium",
            link="https://medium.com/", date_created="2018-12-12"
            )

    def create_inactive_user(self):
        """Create an inactive user."""
        User.objects.create(
            email="timon@gmail.com", first_name="timon", last_name="pumba",
            is_staff=False, is_active=False, is_change_allowed=False,
            country_code=self.country_code, phone_number=722000000
            )
        self.timon = User.objects.get(email="timon@gmail.com")
        self.timon.set_password("secrets")
        self.timon.save()

    def create_color(self):
        """Add phone colors."""
        Color.objects.create(color="Red")
        Color.objects.create(color="RoseGold")
        Color.objects.create(color="Silver")
        self.color_one = Color.objects.get(color="Red")
        self.color_two = Color.objects.get(color="RoseGold")
        self.color_three = Color.objects.get(color="Silver")

    def create_phone_brand(self):
        """
        A method that creates a brand of a phone that can be used with other
        tests.
        """
        PhoneBrand.objects.create(brand_name="Samsung")
        PhoneBrand.objects.create(brand_name="Lg")
        PhoneBrand.objects.create(brand_name="Apple")
        self.samsung_brand = PhoneBrand.objects.get(brand_name="Samsung")
        self.lg_brand = PhoneBrand.objects.get(brand_name="Lg")
        self.apple_brand = PhoneBrand.objects.get(brand_name="Apple")

    def create_phone_model(self):
        """
        A method that creates a model of a phone.
        """
        PhoneModel.objects.create(
            category=self.android, brand=self.samsung_brand,
            brand_model="Samsung Note 5", average_review=5.0)
        self.samsung_note_5 = PhoneModel.objects.get(
            brand_model="Samsung Note 5")
        PhoneModel.objects.create(
            category=self.android, brand=self.samsung_brand,
            brand_model="Samsung Note 7", average_review=5.0)
        self.samsung_note_7 = PhoneModel.objects.get(
            brand_model="Samsung Note 7")
        PhoneModel.objects.create(
            category=self.iphone, brand=self.apple_brand,
            brand_model="Iphone 6 S", average_review=5.0)
        self.iphone_6_s = PhoneModel.objects.get(
            brand_model="Iphone 6 S")

    def create_phone_model_list(self):
        """Create a phone list."""
        PhoneModelList.objects.create(
            phone_model=self.samsung_note_5, currency=self.currency,
            price=25000, size_sku=self.android_size,
            color=self.color_one,
            quantity=4, is_in_stock=True)
        self.samsung_note_5_rose_gold = PhoneModelList.objects.get(
            phone_model=self.samsung_note_5, color=self.color_one
        )
        PhoneModelList.objects.create(
            phone_model=self.samsung_note_7, currency=self.currency,
            price=25000, size_sku=self.android_size,
            color=self.color_one,
            quantity=4, is_in_stock=True)
        self.samsung_note_7_rose_gold = PhoneModelList.objects.get(
            phone_model=self.samsung_note_7, color=self.color_one
        )
        PhoneModelList.objects.create(
            phone_model=self.iphone_6_s, currency=self.currency,
            price=25000, size_sku=self.iphone_size,
            color=self.color_one,
            quantity=4, is_in_stock=True)
        self.iphone_6_s_rose_gold = PhoneModelList.objects.get(
            phone_model=self.iphone_6_s, color=self.color_one
        )

    def tearDown(self):
        """Remove the test environment."""
        cache.clear()
