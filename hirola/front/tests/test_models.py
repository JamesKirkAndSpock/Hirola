from front.base_test import *
from django.db import IntegrityError, DataError


class LandingPageImageModelsTestCase(TestCase):
    def setUp(self):
        LandingPageImage.objects.create(pk=1)
        LandingPageImage.objects.create(phone_name="Phone1",
                                        phone_tag="Phone1_Tag", pk=2,)
        LandingPageImage.objects.create(phone_name="Phone2",
                                        phone_tag="Phone2_Tag", pk=3,)

    def test_that_default_values_are_picked(self):
        """
        Test that a landing page image is created with default values
        """
        get_object = LandingPageImage.objects.get(pk=1)
        self.assertEqual(get_object.carousel_color, 'red')
        self.assertEqual(get_object.text_color, 'white')
        self.assertEqual(get_object.phone_name, '')
        self.assertEqual(get_object.phone_tag, '')

    def test_deletion(self):
        """
        Test that a landing page image can be deleted
        """
        self.assertEqual(len(LandingPageImage.objects.all()), 3)
        get_object = LandingPageImage.objects.get(phone_name="Phone1")
        get_object.delete()
        self.assertEqual(len(LandingPageImage.objects.all()), 2)

    def test_edition(self):
        get_object = LandingPageImage.objects.get(pk=3)
        self.assertEqual(get_object.phone_name, "Phone2")
        self.assertEqual(get_object.phone_tag, "Phone2_Tag")
        get_object.phone_name = "Phone2_Prime"
        get_object.phone_tag = "Phone2_Tag_Prime"
        get_object.save()
        get_edited_object = LandingPageImage.objects.get(pk=3)
        self.assertNotEqual(get_edited_object.phone_name, "Phone2")
        self.assertNotEqual(get_edited_object.phone_tag, "Phone2_Tag")
        self.assertEqual(get_edited_object.phone_name, "Phone2_Prime")
        self.assertEqual(get_edited_object.phone_tag, "Phone2_Tag_Prime")


class PhoneCategoryListModelsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneCategoryListModelsTestCase, self).setUp()

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
            PhoneCategoryList.objects.create(phone_category="Iphone")

    def test_limit_of_phone_category(self):
        '''
        Test that the phone category name is not more that 15 characters.
        The model should raise a data error if this is the case.
        '''
        with self.assertRaises(DataError):
            PhoneCategoryList.objects.create(phone_category="abcdefghijklmnop")


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
