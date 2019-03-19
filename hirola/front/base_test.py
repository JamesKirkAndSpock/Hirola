"""Sets up the environment required for app's tests."""
from hirola.settings.base import BASE_DIR
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from front.models import (
    PhoneCategory, PhoneMemorySize, Currency,
    NewsItem, Color, ItemIcon,
    cache, User, ServicePerson, RepairService, Service,
    CountryCode, PhoneModelList, PhoneBrand, PhoneModel
    )


class BaseTestCase(TestCase):
    """Creates the environment variables required by tests."""

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.create_admin()
        self.create_phone_categories()
        self.create_phone_sizes()
        self.create_currency()
        self.create_landing_page_image()
        self.create_news_item()
        self.create_color()
        self.create_service_men()
        self.create_repair_services()
        self.add_serviceman_services()
        self.create_phone_brand()
        self.create_phone_model()
        self.create_phone_model_list()

    def create_admin(self):
        """Create a super user Elena who has admin privilidges."""
        self.elena = Client()
        user = User.objects.create_superuser(
            email='test@example.com',
            password='test',
        )
        self.elena.force_login(user)

    def create_phone_categories(self):
        """Create Create Phone Categories."""
        phone_list = ["Iphone", "Android", "Tablet"]
        ItemIcon.objects.create(item_icon="icon-test")
        icon = ItemIcon.objects.get(item_icon="icon-test")
        for item in phone_list:
            PhoneCategory.objects.create(phone_category=item,
                                         category_icon=icon)
        self.iphone = PhoneCategory.objects.get(phone_category="Iphone")
        self.android = PhoneCategory.objects.get(phone_category="Android")
        self.tablet = PhoneCategory.objects.get(phone_category="Tablet")

    def create_phone_sizes(self):
        """Create Phone Memory Sizes."""
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
        """Create a currency."""
        Currency.objects.create(currency_abbreviation="V$",
                                currency_long_form="V-dollar")
        self.currency_v = Currency.objects.get(currency_abbreviation="V$")

    def create_news_item(self):
        """Create a news item."""
        NewsItem.objects.create(
            title="Teke rocks",
            source="The standard online",
            link="https://www.sde.com",
            date_created="2018-12-10"
        )
        self.link = NewsItem.objects.get(link="https://www.sde.com")

    def create_color(self):
        """Create colors."""
        Color.objects.create(color="Red")
        Color.objects.create(color="RoseGold")
        Color.objects.create(color="Silver")
        self.color_one = Color.objects.get(color="Red")
        self.color_two = Color.objects.get(color="RoseGold")
        self.color_three = Color.objects.get(color="Silver")

    def create_landing_page_image(self):
        """Create a landing page image."""
        add_url = "/admin/front/landingpageimage/add/"
        mock_image = image('test_image_2.jpeg')
        form = landing_page_form(mock_image, 2, ["red", "white"])
        self.elena.post(add_url, form)

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
            brand_model="Samsung Edge s6", average_review=5.0)
        self.samsung_edge_s6 = PhoneModel.objects.get(
            brand_model="Samsung Edge s6")
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
        PhoneModel.objects.create(
            category=self.android, brand=self.lg_brand,
            brand_model='Lg Plus', average_review=5.0)
        self.lg_plus = PhoneModel.objects.get(
            brand_model="Lg Plus")

    def create_phone_model_list(self):
        """Create Phone models."""
        PhoneModelList.objects.create(
            phone_model=self.samsung_note_5, currency=self.currency_v,
            price=25000, size_sku=self.size_android,
            main_image=image("test_image_5.png"), color=self.color_one,
            quantity=4, is_in_stock=True)
        self.samsung_note_5_rose_gold = PhoneModelList.objects.get(
            phone_model=self.samsung_note_5, color=self.color_one)
        PhoneModelList.objects.create(
            phone_model=self.samsung_note_7, currency=self.currency_v,
            price=25000, size_sku=self.size_android,
            main_image=image("test_image_5.png"), color=self.color_one,
            quantity=4, is_in_stock=True)
        self.samsung_note_7_rose_gold = PhoneModelList.objects.get(
            phone_model=self.samsung_note_7, color=self.color_one
        )
        PhoneModelList.objects.create(
            phone_model=self.iphone_6_s, currency=self.currency_v,
            price=25000, size_sku=self.size_iphone,
            main_image=image("test_image_5.png"), color=self.color_one,
            quantity=4, is_in_stock=True)
        self.iphone_6_s_rose_gold = PhoneModelList.objects.get(
            phone_model=self.iphone_6_s, color=self.color_one
        )
        PhoneModelList.objects.create(
            phone_model=self.lg_plus, currency=self.currency_v,
            price=12000, size_sku=self.size_android,
            main_image=image("test_image_5.png"), color=self.color_three,
            quantity=4, is_in_stock=True)
        self.lg_plus_silver = PhoneModelList.objects.get(
            phone_model=self.lg_plus, color=self.color_three)
        PhoneModelList.objects.create(
            phone_model=self.lg_plus, currency=self.currency_v,
            price=5000, size_sku=self.any_phone_size,
            main_image=image("test_image_5.png"), color=self.color_three,
            quantity=4, is_in_stock=True)
        self.lg_plus_silver_two = PhoneModelList.objects.get(
            phone_model=self.lg_plus, price=5000)

    def create_repair_services(self):
        """Create repair services."""
        RepairService.objects.create(repair_service="Battery replacement")
        self.service_one = RepairService.objects.get(
            repair_service="Battery replacement")
        RepairService.objects.create(repair_service="Unlocking GSM")
        self.service_two = RepairService.objects.get(
            repair_service="Unlocking GSM")

    def add_serviceman_services(self):
        """Associate service with provider."""
        Service.objects.create(service=self.service_one,
                               service_man=self.service_person_one)
        Service.objects.create(service=self.service_two,
                               service_man=self.service_person_one)

    def create_service_men(self):
        """Create service provider."""
        self.code = CountryCode.objects.all().first()
        ServicePerson.objects.create(
            first_name="Wanjigi",
            name_of_premise="Cutting Edge Tec",
            country_code=self.code,
            phone_number="715557775"
            )
        self.service_person_one = ServicePerson.objects.\
            get(first_name="Wanjigi")

    def tearDown(self):
        cache.clear()


def landing_page_form(image, num, color):
    """
    Create a mock landing page form data.
    """
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
    """
    Create an image.

    Parameters:
        name(str): name of the image

    Returns:
        image
    """
    image_path = BASE_DIR + '/media/' + name
    mock_image = SimpleUploadedFile(
        name=name,
        content=open(image_path, 'rb').read(),
        content_type='image/jpeg'
        )
    return mock_image
