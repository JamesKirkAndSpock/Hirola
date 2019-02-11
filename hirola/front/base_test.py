import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from hirola.settings.base import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from front.models import (PhoneCategory, PhoneMemorySize, Currency,
                          NewsItem, Color, PhonesColor, ItemIcon, PhoneList,
                          cache, CountryCode, HotDeal, Feature, Review,
                          get_default, ProductInformation, Order, OrderStatus,
                          PhoneImage, User, Cart, ShippingAddress, SocialMedia, InactiveUser)


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.create_admin()
        self.create_phone_categories()
        self.create_phone_sizes()
        self.create_currency()
        self.create_landing_page_image()
        self.create_phones()
        self.create_news_item()
        self.create_color()
        self.add_phone_colors()

    def create_admin(self):
        # Elena is an admin who has admin privilidges
        self.elena = Client()
        user = User.objects.create_superuser(
            email='test@example.com',
            password='test',
        )
        self.elena.force_login(user)

    def create_phone_categories(self):
        # Create Phone Categories
        phone_list = ["Iphone", "Android", "Tablet"]
        for item in phone_list:
            PhoneCategory.objects.create(phone_category=item)
        self.iphone = PhoneCategory.objects.get(phone_category="Iphone")
        self.android = PhoneCategory.objects.get(phone_category="Android")
        self.tablet = PhoneCategory.objects.get(phone_category="Tablet")

    def create_phone_sizes(self):
        # Create Phone Memory Sizes
        data = {self.iphone: [8], self.android: [16], self.tablet: [24]}
        for key in data:
            PhoneMemorySize.objects.create(abbreviation="GB",
                                           size_number=data[key][0],
                                           category=key)
        self.size_iphone = PhoneMemorySize.objects.get(
            category=self.iphone)
        self.size_android = PhoneMemorySize.objects.get(
            category=self.android)
        self.size_tablet = PhoneMemorySize.objects.get(
            category=self.tablet)
        PhoneMemorySize.objects.create(abbreviation="GB",
                                       size_number=4)
        self.any_phone_size = PhoneMemorySize.objects.get(size_number=4)

    def create_currency(self):
        # Create a currency
        Currency.objects.create(currency_abbreviation="V$",
                                currency_long_form="V-dollar")
        self.currency_v = Currency.objects.get(currency_abbreviation="V$")

    def create_news_item(self):
        NewsItem.objects.create(
            title="Teke rocks",
            source="The standard online",
            link="https://www.sde.com",
            date_created="2018-12-10"
        )
        self.link = NewsItem.objects.get(link="https://www.sde.com")

    def create_color(self):
        Color.objects.create(color="Red")
        Color.objects.create(color="RoseGold")
        Color.objects.create(color="Silver")
        self.color_one = Color.objects.get(color="Red")
        self.color_two = Color.objects.get(color="RoseGold")
        self.color_three = Color.objects.get(color="Silver")

    def add_phone_colors(self):

        PhonesColor.objects.create(
            phone=self.iphone_6, size=self.size_iphone, price=10000,
            color=self.color_one, quantity=5, is_in_stock=True)
        PhonesColor.objects.create(
            phone=self.iphone_6, size=self.any_phone_size, price=10000,
            color=self.color_two, quantity=10, is_in_stock=True)
        self.iphone6_colors = PhonesColor.objects.filter(phone=self.iphone_6.pk)
        self.all_colors = PhonesColor.objects.all()

    def create_landing_page_image(self):
        add_url = "/admin/front/landingpageimage/add/"
        mock_image = image('test_image_2.jpeg')
        form = landing_page_form(mock_image, 2, ["red", "white"])
        self.elena.post(add_url, form)

    def create_phones(self):
        ItemIcon.objects.create(item_icon="apple")
        icon = ItemIcon.objects.get(item_icon="apple")
        PhoneList.objects.create(category=self.iphone, currency=self.currency_v,
                                 price=300000, phone_name="Iphone 6", icon=icon,
                                 main_image=image("test_image_5.png"))
        self.iphone_6 = PhoneList.objects.get(phone_name="Iphone 6")
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=250000, phone_name="Samsung J7")
        self.samsung_j_7 = PhoneList.objects.get(phone_name="Samsung J7")

    def tearDown(self):
        cache.clear()


def landing_page_form(image, num, color):
    if isinstance(num, int):
        form = {"photo": image, "carousel_color": color[0],
                "phone_name": "test_phone_name{}".format(num),
                "phone_tag": "test_phone_tag{}".format(num),
                "text_color": color[1]}
    else:
        phone_name = num[0]
        phone_tag = num[1]
        form = {"photo": image, "carousel_color": color[0],
                "phone_name": phone_name, "phone_tag": phone_tag,
                "text_color": color[1]}
    return form


def image(name):
    image_path = BASE_DIR + '/media/' + name
    mock_image = SimpleUploadedFile(name=name,
                                    content=open(image_path, 'rb').read(),
                                    content_type='image/jpeg')
    return mock_image
