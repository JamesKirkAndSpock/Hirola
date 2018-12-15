from front.base_test import *
from django.db import IntegrityError, DataError
from front.errors import *


class PhoneCategoryModelsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneCategoryModelsTestCase, self).setUp()

    def test_object_returned_string(self):
        '''
        Test that when getting an object of a model for the Phone Category List
        It is possible to get a string representation of the object that is
        human readable.
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
        response = self.elena.post("/admin/front/phonecategory/{}/change/".format(self.iphone.pk),
                                   form)
        self.assertRedirects(response, "/admin/front/phonecategory/", 302)


class PhoneMemorySizeModelsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneMemorySizeModelsTestCase, self).setUp()

    def test_object_returned_correct_string(self):
        '''
        Test that the object returns a string that has both the size number and
        appreviation
        '''
        output = str(self.size_tablet)
        self.assertEqual(output, "24 GB")


class CurrencyModelTestCase(BaseTestCase):
    def setUp(self):
        super(CurrencyModelTestCase, self).setUp()

    def test_it_returns_string(self):
        '''
        Test that the currency value returned for an object of currecny will be
        a string that is human readable
        '''
        self.assertEqual(str(self.currency_v), "V$")


class PhoneListModelTestCase(TestCase):
    def test_that_phone_name_is_necessary(self):
        with self.assertRaises(IntegrityError):
            PhoneList.objects.create(price=10)

    def test_limit_of_phone_name(self):
        with self.assertRaises(DataError):
            PhoneList.objects.create(phone_name="abcdefghijklmnopqrstuvwxy")


class HotDealModelsTestCase(BaseTestCase):
    def setUp(self):
        super(HotDealModelsTestCase, self).setUp()

    def test_uniqueness_of_hot_deal_category(self):
        '''
        Test that if a Hot Deal object already exists and I create another one with the same Phone
        object
            - That a validation error is raised
        '''
        HotDeal.objects.create(item=self.iphone_6)
        response = self.elena.post("/admin/front/hotdeal/add/", {"item": self.iphone_6.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, hot_deal_error.format(self.iphone_6))


class NewsItemsTestCase(BaseTestCase):
    def setUp(self):
        super(NewsItemsTestCase, self).setUp()

    def test_object_returned_correct_link(self):
        """Test that the object returns the correct link."""
        self.assertEqual(str(self.link), "https://www.sde.com")
