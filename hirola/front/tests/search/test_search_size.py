from front.base_test import *


class SearchSizeTest(BaseTestCase):

    def setUp(self):
        super(SearchSizeTest, self).setUp()
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="LG Razor J7", size_sku=self.size_android)
        self.lg_razor = PhoneList.objects.get(phone_name="LG Razor J7")
        PhonesColor.objects.create(phone=self.lg_razor, quantity=1, is_in_stock=True, color=self.color_one)
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="Samsung S8", size_sku=self.size_android)
        self.samsung_s8 = PhoneList.objects.get(phone_name="Samsung S8")
        PhonesColor.objects.create(phone=self.samsung_s8, quantity=0, is_in_stock=True, color=self.color_one)
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="Samsung Note 5", size_sku=self.size_android)
        self.samsung_n5 = PhoneList.objects.get(phone_name="Samsung Note 5")
        PhonesColor.objects.create(phone=self.samsung_n5, quantity=1, is_in_stock=False, color=self.color_one)


    def test_search_phone_size_button(self):
        '''
        Test that when you search for phones with a particular size:
            - That the page will render phones that have a quantity greater than 1 and that
            have the variable is_in_stock set to True 
        '''
        search_url = "/phone_category/{}/{}/".format(self.android.pk, self.size_android.pk)
        response = self.client.get(search_url)
        self.assertNotContains(response, "Oops! We currently do not have it")
        self.assertContains(response, "LG Razor J7")
        self.assertNotContains(response, "Samsung S8")
        self.assertNotContains(response, "Samsung Note 5")
