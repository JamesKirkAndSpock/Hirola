from front.base_test import (BaseTestCase, image, TestCase)
from django.db import IntegrityError, DataError
from front.errors import hot_deal_error
from front.models import (PhoneCategory, get_default, PhoneList,
                          HotDeal, User, CountryCode, Order, OrderStatus,
                          ShippingAddress, PhonesColor, Color, Cart,
                          ServicePerson, RepairService, Services, Address)

class PhoneCategoryModelsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneCategoryModelsTestCase, self).setUp()

    def test_object_returned_string(self):
        '''
        Test that when getting an object of a model for the
        Phone Category List It is possible to get a string representation
        of the object that is human readable.
        '''
        self.assertEqual(str(self.iphone), "Iphone")

    def test_uniqueness_of_phone_category(self):
        '''
        Test that when creating a new Phone Category that it does not work.
        Test that an integrity error is raised
        '''
        with self.assertRaises(IntegrityError):
            PhoneCategory.objects.create(phone_category="Iphone")

    def test_limit_of_phone_category(self):
        '''
        Test that the phone category name is not more that 15 characters.
        The model should raise a data error if this is the case.
        '''
        with self.assertRaises(DataError):
            PhoneCategory.objects.create(phone_category="abcdefghijklmnop")

    def test_phone_category_edit(self):
        '''
        Test that when a phone category is edited:
            - The page redirects successfully
        '''
        mock_image = image('test_image_6.png')
        form = {"phone_category": "Iphone", "category_image": mock_image}
        response = self.elena.post("/admin/front/phonecategory/{}/change/".
                                   format(self.iphone.pk), form)
        self.assertRedirects(response, "/admin/front/phonecategory/", 302)


class PhoneMemorySizeModelsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneMemorySizeModelsTestCase, self).setUp()

    def test_object_returned_correct_string(self):
        '''
        Test that the object returns a string that has both the
        size number and abbreviation
        '''
        output = str(self.size_tablet)
        self.assertEqual(output, "24 GB")


class CurrencyModelTestCase(BaseTestCase):
    def setUp(self):
        super(CurrencyModelTestCase, self).setUp()

    def test_it_returns_string(self):
        '''
        Test that the currency value returned for an object of
        currecny will be a string that is human readable
        '''
        self.assertEqual(str(self.currency_v), "V$")


class PhoneListModelTestCase(TestCase):
    def test_that_phone_name_is_necessary(self):
        with self.assertRaises(IntegrityError):
            PhoneList.objects.create(price=10)


class HotDealModelsTestCase(BaseTestCase):
    def setUp(self):
        super(HotDealModelsTestCase, self).setUp()

    def test_uniqueness_of_hot_deal_category(self):
        '''
        Test that if a Hot Deal object already exists and I create another
        one with the same Phone object
            - That a validation error is raised
        '''
        HotDeal.objects.create(item=self.iphone_6)
        response = self.elena.post("/admin/front/hotdeal/add/",
                                   {"item": self.iphone_6.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, hot_deal_error.format(self.iphone_6))


class NewsItemsTestCase(BaseTestCase):
    def setUp(self):
        super(NewsItemsTestCase, self).setUp()

    def test_object_returned_correct_link(self):
        """Test that the object returns the correct link."""
        self.assertEqual(str(self.link), "https://www.sde.com")


class UserModelsTestCase(BaseTestCase):

    def setUp(self):
        self.country_code = get_default()
        super(UserModelsTestCase, self).setUp()

    def test_admin_created_with_country_code(self):
        '''
        Test that when an admin is created:
            - The admin automatically gets assigned the default country code.
            This is to prevent any bugs that may be created in case an admin
            visits the dashboard page.
        '''
        admin = User.objects.get(email='test@example.com')
        self.assertEqual(admin.country_code, self.country_code)

    def test_user_created_with_country_code(self):
        '''
        Test that when a normal user of the webapp gets created:
            - That the user automatically gets assigned the default country code.
        '''
        user = User.objects.create_user(email="equatorial@gmail.com",
                                        password="secret")
        self.assertEqual(user.country_code, self.country_code)


class CountryCodeModelsTestCase(BaseTestCase):

    def setUp(self):
        super(CountryCodeModelsTestCase, self).setUp()

    def test_country_code_uniqueness(self):
        '''
        Test that when you create an country code that has either the same
        country code number or country:
            - That an error is raised on uniqueness
        '''
        with self.assertRaises(IntegrityError):
            CountryCode.objects.create(country_code=254, country="Kenya")


class OrderModelsTestCase(BaseTestCase):

    def setUp(self):
        super(OrderModelsTestCase, self).setUp()

    def test_get_address_method(self):
        '''
        Test that when you access the get_address method:
            - That it returns None if a Shipping address does not have one.
            - That it returns the shipping address if an order has one.
        '''
        User.objects.create_user(email="example@gmail.com")
        owner = User.objects.get(email="example@gmail.com")
        PhoneList.objects.create(category=self.android,
                                 size_sku=self.size_android, price=25000,
                                 main_image=image('test_image_5.png'),
                                 phone_name="Samsung",
                                 currency=self.currency_v)
        OrderStatus.objects.create(status="Pending")
        Cart.objects.create(owner=None)
        cart = Cart.objects.get(owner=None)
        phone = PhoneList.objects.get(phone_name="Samsung")
        status = OrderStatus.objects.get(status="Pending")
        Order.objects.create(
            owner=owner, phone=phone, status=status,
            quantity=2, price=25000, total_price=80000, cart=cart)
        order = Order.objects.get(owner=owner)
        self.assertEqual(order.get_address, None)
        ShippingAddress.objects.create(order=order, location="Kiambu Road",
                                       pickup="Evergreen Center")
        self.assertEqual(order.get_address.location, "Kiambu Road")

class PhonesColorTestCase(BaseTestCase):

    def setUp(self):
        super(PhonesColorTestCase, self).setUp()

    def test_create_phone_color_object_success(self):
        """Test user can create a phone color object successfuly."""
        PhoneList.objects.create(category=self.android,
                                 size_sku=self.size_android, price=25000,
                                 main_image=image('test_image_5.png'),
                                 phone_name="Samsung",
                                 currency=self.currency_v)
        phone = PhoneList.objects.get(phone_name="Samsung")
        PhonesColor.objects.create(
            phone=phone, size=self.size_android, price=10000,
            quantity=10, is_in_stock=True)
        phone_color = PhonesColor.objects.filter(phone=phone).first()
        self.assertEqual(str(phone_color), "16 GB")
        self.assertEqual(phone_color.price, 10000)
        self.assertEqual(phone_color.phone, phone)
        Color.objects.create(color="White")
        color = Color.objects.get(color="White")
        PhoneList.objects.create(category=self.iphone,
                                 size_sku=self.size_iphone, price=25000,
                                 main_image=image('test_image_5.png'),
                                 phone_name="Iphone X",
                                 currency=self.currency_v)
        phone_2 = PhoneList.objects.get(phone_name="Iphone X")
        PhonesColor.objects.create(
            phone=phone_2, size=self.size_iphone, price=10000,
            color=color, quantity=10, is_in_stock=True)
        phone_color = PhonesColor.objects.filter(phone=phone_2).first()
        self.assertEqual(str(phone_color), "White 8 GB")
        self.assertEqual(phone_color.price, 10000)
        self.assertEqual(phone_color.phone, phone_2)


class ServicesNetworkTestCase(BaseTestCase):

    def setUp(self):
        super(ServicesNetworkTestCase, self).setUp()

    def test_model_creates_service_man(self):
        code = CountryCode.objects.first()
        ServicePerson.objects.create(first_name="Wanjigi",
                                     name_of_premise="Cutting Edge Tec",
                                     country_code=code,
                                     phone_number="715777587")
        service_man = ServicePerson.objects.filter(first_name="Wanjigi").\
            first()
        self.assertEqual(str(service_man), "Wanjigi")
        RepairService.objects.create(service="LED screen Repair")
        repair_service = RepairService.objects.\
            filter(service="LED screen Repair").first()
        self.assertEqual(str(repair_service), "LED screen Repair")
        Services.objects.create(service=repair_service,
                                service_man=self.service_person_one)
        service = Services.objects.filter(service=repair_service).first()
        self.assertEqual(str(service.service_man), "Wanjigi")

    def test_assign_same_service_to_same_service_man_twice_error(self):
        with self.assertRaises(IntegrityError):
            Services.objects.create(service=self.service_one,
                                    service_man=self.service_person_one)


class AddressModelTestCase(BaseTestCase):

    def setUp(self):
        super(AddressModelTestCase, self).setUp()

    def test_create_valid_address(self):
        Address.objects.create(address_line_one="P.O.Box 2354 - 00100",
                               address_line_two="Nairobi")
        address_one = Address.objects.get(address_line_two="Nairobi")
        created_address = "P.O.Box 2354 - 00100" + "\n" + "Nairobi"
        self.assertEqual(str(address_one), created_address)
        Address.objects.create(address_line_one="P.O.Box 30305 - 00100",
                               address_line_two="Mbagathi",
                               address_line_three="Nairobi")
        created_address_two = "P.O.Box 30305 - 00100" + "\n" +\
            "Mbagathi" + "\n" + "Nairobi"
        address_two = Address.objects.get(address_line_two="Mbagathi")
        self.assertEqual(str(address_two), created_address_two)
