from front.base_test import (BaseTestCase, PhoneList, PhonesColor, Client)
from front.models import (Feature, Review, ProductInformation, User, PhoneModel, PhoneModelList)


class SearchTest(BaseTestCase):

    def setUp(self):
        User.objects.create_user(email="sivanna@gmail.com",
                                 password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.sivanna = Client()
        super(SearchTest, self).setUp()

    def test_search_get_request(self):
        '''
        Test that when you use a get method to request for the search page
            - That the page redirects to the landing page
        '''
        response = self.sivanna.get("/search")
        self.assertContains(response, "Add something to the search bar to"
                            " search for your items")

    def test_search_phone_name(self):
        '''
        Test that when you search for a phone name:
            - That the phone object is rendered on the search response
        '''
        response = self.sivanna.post("/search", {"search-name": "sam"})
        self.assertContains(response, self.samsung_note_5_rose_gold.phone_model)

    def test_search_phone_price(self):
        '''
        Test that whe you search for a phone price:
            - That the phone object is rendered on the search response
        '''
        response = self.sivanna.post("/search", {"search-name": "25"})
        self.assertContains(response, self.samsung_note_5_rose_gold.phone_model)

    def test_search_phone_size(self):
        '''
        Test that when you search for a phone price:
            - That the phone object is rendered on the search response
        '''
        response = self.sivanna.post("/search", {"search-name": "16"})
        self.assertContains(response, self.samsung_note_5_rose_gold.phone_model)

    def test_search_phone_category(self):
        '''
        Test that when you enter a category name in the search bar:
            - That you get phone objects in that category
        '''
        response = self.sivanna.post("/search", {"search-name": "andro"})
        self.assertContains(response, self.samsung_note_5_rose_gold.phone_model)
        self.assertContains(response, self.samsung_note_7_rose_gold.phone_model)
        self.assertNotContains(response, self.iphone_6_s_rose_gold.phone_model)

    def test_search_phone_feature(self):
        '''
        Test that when you enter a phone feature in the search bar:
            - That you get phone objects with that feature
        '''

        Feature.objects.create(phone=self.samsung_note_7_rose_gold,
                               feature="6-inch screen")
        Feature.objects.create(phone=self.iphone_6_s_rose_gold, feature="7-inch screen")
        response = self.sivanna.post("/search", {"search-name": "inch"})
        self.assertContains(response, self.samsung_note_7_rose_gold.phone_model)
        self.assertContains(response, self.iphone_6_s_rose_gold.phone_model)
        self.assertNotContains(response, self.samsung_note_5_rose_gold.phone_model)

    def test_search_product_information(self):
        '''
        Test that when you enter a phone product information in the \
            search bar:
            - That you get phone objects with that product information
        '''
        ProductInformation.objects.create(phone=self.samsung_note_7_rose_gold,
                                          feature="Network", value="GSM")
        ProductInformation.objects.create(phone=self.iphone_6_s_rose_gold,
                                          feature="Network", value="GSM")
        response = self.sivanna.post("/search", {"search-name": "gsm"})
        self.assertContains(response, self.samsung_note_7_rose_gold.phone_model)
        self.assertContains(response, self.iphone_6_s_rose_gold.phone_model)
        self.assertNotContains(response, self.samsung_note_5_rose_gold.phone_model)
        response_2 = self.sivanna.post("/search", {"search-name": "net"})
        self.assertContains(response, self.samsung_note_7_rose_gold.phone_model)
        self.assertContains(response, self.iphone_6_s_rose_gold.phone_model)
        self.assertNotContains(response, self.samsung_note_5_rose_gold.phone_model)

    def test_search_product_review(self):
        '''
        Test that when you enter a phone review in the search bar:
            - That you get phone objects with that product information
        '''
        authentic_comment = "That was an authentic phone that I got"
        genuine_comment = "That was an genuine phone that I got"
        Review.objects.create(stars=5, comments=authentic_comment,
                              phone_model=self.samsung_note_5, owner=self.user)
        Review.objects.create(stars=4, comments=genuine_comment,
                              phone_model=self.samsung_note_7, owner=self.user)
        response = self.sivanna.post("/search", {"search-name": "genui"})
        self.assertNotContains(response, self.samsung_note_5_rose_gold.phone_model)
        self.assertContains(response, self.samsung_note_7_rose_gold.phone_model)
        self.assertNotContains(response, self.iphone_6_s_rose_gold.phone_model)
        response_2 = self.sivanna.post("/search", {"search-name": "auth"})
        self.assertContains(response_2, self.samsung_note_5_rose_gold.phone_model)
        self.assertNotContains(response_2, self.samsung_note_7_rose_gold.phone_model)
        self.assertNotContains(response_2, self.iphone_6_s_rose_gold.phone_model)

    def test_not_in_stock_search(self):
        '''
        Test that for phones that are not in stock, or their quantity is zero:
            - They won't be rendered on search
        '''
        PhoneModel.objects.create(
            category=self.iphone, brand=self.apple_brand,
            brand_model="Iphone 6 J", average_review=5.0)
        self.iphone_6_j = PhoneModel.objects.get(
            brand_model="Iphone 6 J")
        PhoneModel.objects.create(
            category=self.iphone, brand=self.apple_brand,
            brand_model="Iphone 7 J", average_review=5.0)
        self.iphone_7_j = PhoneModel.objects.get(
            brand_model="Iphone 7 J")
        PhoneModelList.objects.create(
            phone_model=self.iphone_6_j, currency=self.currency_v,
            price=25000, size_sku=self.size_iphone, color=self.color_one,
            quantity=0, is_in_stock=True)
        self.iphone_6_s_rose_gold = PhoneModelList.objects.get(
            phone_model=self.iphone_6_s, color=self.color_one
        )
        PhoneModelList.objects.create(
            phone_model=self.iphone_7_j, currency=self.currency_v,
            price=25000, size_sku=self.size_iphone, color=self.color_one,
            quantity=4, is_in_stock=False)
        self.iphone_7_s_rose_gold = PhoneModelList.objects.get(
            phone_model=self.iphone_7_j, color=self.color_one
        )
        post_response_1 = self.client.post("/search",
                                           {"search-name": "Samsung Note 5"})
        post_response_3 = self.client.post("/search", {"search-name": "Iphone 6 J"})
        post_response_2 = self.client.post("/search", {"search-name": "Iphone 7"})
        self.assertContains(post_response_1, "Samsung Note 5")
        self.assertNotContains(post_response_2, "Iphone 7")
        self.assertNotContains(post_response_3, "Iphone 6")
