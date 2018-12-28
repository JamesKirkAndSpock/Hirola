from front.base_test import *


class SearchTest(BaseTestCase):

    def setUp(self):
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.sivanna = Client()
        super(SearchTest, self).setUp()
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="LG Razor J7")
        self.lg_razor = PhoneList.objects.get(phone_name="LG Razor J7")
        PhonesColor.objects.create(phone=self.lg_razor, color=self.color_one, quantity=1, is_in_stock=True)
        PhonesColor.objects.create(phone=self.samsung_j_7, color=self.color_one, quantity=1, is_in_stock=True)

    def test_search_get_request(self):
        '''
        Test that when you use a get method to request for the search page
            - That the page redirects to the landing page
        '''
        response = self.sivanna.get("/search")
        self.assertContains(response, "Add something to the search bar to search for your items")

    def test_search_phone_name(self):
        '''
        Test that when you search for a phone name:
            - That the phone object is rendered on the search response
        '''
        response = self.sivanna.post("/search", {"search-name": "sam"})
        self.assertContains(response, self.samsung_j_7.phone_name)

    def test_search_phone_price(self):
        '''
        Test that whe you search for a phone price:
            - That the phone obeject is rendered on the search response
        '''
        response = self.sivanna.post("/search", {"search-name": "25"})
        self.assertContains(response, self.samsung_j_7.phone_name)

    def test_search_phone_size(self):
        '''
        Test that when you search for a phone price:
            - That the phone object is rendered on the search response
        '''
        self.lg_razor.size_sku = self.size_android
        self.lg_razor.save()
        response = self.sivanna.post("/search", {"search-name": "16"})
        self.assertContains(response, self.lg_razor.phone_name)

    def test_search_phone_category(self):
        '''
        Test that when you enter a category name in the search bar:
            - That you get phone objects in that category
        '''
        response = self.sivanna.post("/search", {"search-name": "andro"})
        self.assertContains(response, self.samsung_j_7.phone_name)
        self.assertContains(response, self.lg_razor.phone_name)
        self.assertNotContains(response, self.iphone_6.phone_name)

    def test_search_phone_feature(self):
        '''
        Test that when you enter a phone feature in the search bar:
            - That you get phone objects with that feature
        '''

        Feature.objects.create(phone=self.samsung_j_7, feature="6-inch screen")
        Feature.objects.create(phone=self.lg_razor, feature="7-inch screen")
        response = self.sivanna.post("/search", {"search-name": "inch"})
        self.assertContains(response, self.samsung_j_7.phone_name)
        self.assertContains(response, self.lg_razor.phone_name)
        self.assertNotContains(response, self.iphone_6)

    def test_search_product_information(self):
        '''
        Test that when you enter a phone product information in the search bar:
            - That you get phone objects with that product information
        '''
        ProductInformation.objects.create(phone=self.samsung_j_7, feature="Network", value="GSM")
        ProductInformation.objects.create(phone=self.lg_razor, feature="Network", value="GSM")
        response = self.sivanna.post("/search", {"search-name": "gsm"})
        self.assertContains(response, self.samsung_j_7.phone_name)
        self.assertContains(response, self.lg_razor.phone_name)
        self.assertNotContains(response, self.iphone_6)
        response_2 = self.sivanna.post("/search", {"search-name": "net"})
        self.assertContains(response_2, self.samsung_j_7.phone_name)
        self.assertContains(response_2, self.lg_razor.phone_name)
        self.assertNotContains(response_2, self.iphone_6)

    def test_search_product_review(self):
        '''
        Test that when you enter a prone review in the search bar:
            - That you get phone objects with that product information
        '''
        authentic_comment = "That was an authentic phone that I got"
        genuine_comment = "That was an genuine phone that I got"
        Review.objects.create(stars=5, comments=authentic_comment, phone=self.samsung_j_7,
                              owner=self.user)
        Review.objects.create(stars=4, comments=genuine_comment, phone=self.lg_razor,
                              owner=self.user)
        response = self.sivanna.post("/search", {"search-name": "genui"})
        self.assertNotContains(response, self.samsung_j_7.phone_name)
        self.assertContains(response, self.lg_razor.phone_name)
        self.assertNotContains(response, self.iphone_6)
        response_2 = self.sivanna.post("/search", {"search-name": "auth"})
        self.assertContains(response_2, self.samsung_j_7.phone_name)
        self.assertNotContains(response_2, self.lg_razor.phone_name)
        self.assertNotContains(response_2, self.iphone_6)

    def test_not_in_stock_search(self):
        '''
        Test that for phones that are not in stock, or their quantity is zero:
            - They won't be rendered on search
        '''
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="Samsung S8", size_sku=self.size_android)
        self.samsung_s8 = PhoneList.objects.get(phone_name="Samsung S8")
        PhonesColor.objects.create(phone=self.samsung_s8, quantity=0, is_in_stock=True, color=self.color_one)
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=8000, phone_name="Samsung Note 5", size_sku=self.size_android)
        self.samsung_n5 = PhoneList.objects.get(phone_name="Samsung Note 5")
        PhonesColor.objects.create(phone=self.samsung_n5, quantity=1, is_in_stock=False, color=self.color_one)
        post_response_1 = self.client.post("/search", {"search-name": "LG Raz"})
        post_response_3 = self.client.post("/search", {"search-name": "Note"})
        post_response_2 = self.client.post("/search", {"search-name": "S8"})
        self.assertContains(post_response_1, "LG Razor J7")
        self.assertNotContains(post_response_2, "Samsung S8")
        self.assertNotContains(post_response_3, "Samsung Note 5")
