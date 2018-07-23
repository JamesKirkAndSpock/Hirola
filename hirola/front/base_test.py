import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from hirola.settings.base import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from front.models import *


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.create_admin()
        self.create_phone_categories()
        self.create_phone_sizes()
        self.create_currency()
        self.create_landing_page_image()

    def create_admin(self):
        # Elena is an admin who has admin privilidges
        self.elena = Client()
        user = User.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='test',
        )
        self.elena.force_login(user)

    def create_phone_categories(self):
        # Create Phone Categories
        phone_list = ["Iphone", "Android", "Tablet"]
        for item in phone_list:
            PhoneCategoryList.objects.create(phone_category=item)
        self.iphone = PhoneCategoryList.objects.get(phone_category="Iphone")
        self.android = PhoneCategoryList.objects.get(phone_category="Android")
        self.tablet = PhoneCategoryList.objects.get(phone_category="Tablet")

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

    def create_currency(self):
        # Create a currency
        Currency.objects.create(currency_abbreviation="V$",
                                currency_long_form="V-dollar")
        self.currency_v = Currency.objects.get(currency_abbreviation="V$")

    def create_landing_page_image(self):
        add_url = "/admin/front/landingpageimage/add/"
        mock_image = image('test_image_2.jpeg')
        form = landing_page_form(mock_image, 2, ["red", "white"])
        self.elena.post(add_url, form)


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
