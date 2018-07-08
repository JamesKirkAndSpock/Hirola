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
                                           size_category=key)
        self.size_iphone = PhoneMemorySize.objects.get(
            size_category=self.iphone)
        self.size_android = PhoneMemorySize.objects.get(
            size_category=self.android)
        self.size_tablet = PhoneMemorySize.objects.get(
            size_category=self.tablet)

    def create_currency(self):
        # Create a currency
        Currency.objects.create(currency_abbreviation="V$",
                                currency_long_form="V-dollar")
        self.currency_v = Currency.objects.get(currency_abbreviation="V$")
