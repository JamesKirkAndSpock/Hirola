from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from front.models import *


class BaseSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        super(BaseSeleniumTestCase, self).setUp()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.create_social_media()
        self.create_phone_category()
        self.create_phone_memory_size()
        self.create_currency()
        self.create_item_icon()
        self.create_phone_list()

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
        PhoneList.objects.create(
            category=self.android, phone_name="Android Example1", currency=self.currency,
            price=35000.00, size_sku=self.android_size,
            icon=self.android_icon, average_review=4.0, main_image="phones/test_image_5.png"
        )

    def tearDown(self):
        cache.clear()