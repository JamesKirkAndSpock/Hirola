from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from front.models import *


class BaseSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        super(BaseSeleniumTestCase, self).setUp()

    def create_social_media(self):
        SocialMedia.objects.create(url_link="https://facebook.com", icon="fa fa-facebook",
                                   name="Facebook")
        SocialMedia.objects.create(url_link="https://instagram.com", icon="fa fa-instagram",
                                   name="Instagram")

    def create_phone_category(self):
        PhoneCategory.objects.create(phone_category="iPhone",
                                     category_image="phone_categories/test_image_6.png")
        self.iphone = PhoneCategory.objects.get(phone_category="iPhone")
        PhoneCategory.objects.create(phone_category="Android",
                                     category_image="phone_categories/test_image_6.png")
        self.android = PhoneCategory.objects.get(phone_category="Android")

    def create_phone_memory_size(self):
        PhoneMemorySize.objects.create(abbreviation="GB", size_number=8, category=self.iphone)
        self.iphone_size = PhoneMemorySize.objects.get(category=self.iphone)
        PhoneMemorySize.objects.create(abbreviation="GB", size_number=16, category=self.android)
        self.android_size = PhoneMemorySize.objects.get(category=self.iphone)

    def create_currency(self):
        Currency.objects.create(currency_abbreviation="Kshs.",
                                currency_long_form="Kenya Shillings")
        self.currency = Currency.objects.get(currency_abbreviation="Kshs.")

    def create_item_icon(self):
        ItemIcon.objects.create(item_icon="iphone")
        self.iphone_icon = ItemIcon.objects.get(item_icon="iphone")
        ItemIcon.objects.create(item_icon="android")
        self.android_icon = ItemIcon.objects.get(item_icon="android")

    def create_phone_list(self):
        PhoneList.objects.create(
            category=self.iphone, phone_name="iPhone Example1", currency=self.currency,
            price=25000.00, size_sku=self.iphone_size, icon=self.iphone_icon, average_review=5.0,
            main_image="phones/test_image_5.png"
        )
        self.iphone_example = PhoneList.objects.get(phone_name="iPhone Example1")
        PhoneList.objects.create(
            category=self.android, phone_name="Android Example1", currency=self.currency,
            price=35000.00, size_sku=self.android_size,
            icon=self.android_icon, average_review=4.0, main_image="phones/test_image_5.png"
        )
        self.android_example = PhoneList.objects.get(phone_name="Android Example1")

    def create_country_code(self):
        CountryCode.objects.create(country_code=254, country="Kenya")
        self.country_code = CountryCode.objects.get(country="Kenya")

    def create_user(self):
        User.objects.create(email="timonpumba@gmail.com", first_name="timon", last_name="pumba",
                            is_staff=True, is_active=True,is_change_allowed=False,
                            country_code=self.country_code, phone_number=722000000)
        self.timon = User.objects.get(email="timonpumba@gmail.com")
        self.timon.set_password("secret")
        self.timon.save()

    def create_order_status(self):
        OrderStatus.objects.create(status="Pending")
        self.order_status = OrderStatus.objects.get(status="Pending")

    def create_payment_method(self):
        PaymentMethod.objects.create(payment_method="Mpesa")
        self.mpesa = PaymentMethod.objects.get(payment_method="Mpesa")

    def create_order(self):
        Order.objects.create(owner=self.timon, phone=self.iphone_example, status=self.order_status,
                             quantity=2, total_price=20000, payment_method=self.mpesa,
                             date="2018-12-12")
        self.order = Order.objects.get(owner=self.timon)

    def create_shipping_address(self):
        ShippingAddress.objects.create(order=self.order, pickup="Evergreen Center",
                                       location="Kiambu Road", recepient="Nala")

    def create_news(self):
        NewsItem.objects.create(title="Teke rocks", source="Medium",
                                link="https://medium.com/", date_created="2018-12-12")

    def create_inactive_user(self):
        User.objects.create(email="timon@gmail.com", first_name="timon", last_name="pumba",
                            is_staff=False, is_active=False, is_change_allowed=False,
                            country_code=self.country_code, phone_number=722000000)
        self.timon = User.objects.get(email="timon@gmail.com")
        self.timon.set_password("secrets")
        self.timon.save()

    def tearDown(self):
        cache.clear()
