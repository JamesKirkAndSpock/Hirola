from front.base_test import *


class PhoneProfileTemplate(BaseTestCase):
    '''
    Test that templates render the correct information due to objects added on
    the database
    '''
    def setUp(self):
        User.objects.create(email="example@gmail.com", first_name="Example",
                            last_name="User", is_staff=False, is_active=True,
                            is_change_allowed=False, phone_number=72200000,
                            photo=image("test_image_5.png") )
        self.user = User.objects.get(first_name="Example")
        super(PhoneProfileTemplate, self).setUp()

    def test_customer_reviews_rendered(self):
        '''
        Test that when you visit a page for a profile which a customer has
        reviewed:
        - That the page renders the customer name
        - That the page renders the number of stars he had rated on the review
        - That the page renders his review comment
        - That the page renders the date he reviewed
        '''
        review = Review.objects.create(stars=4, comments="Good job guys", phone=self.iphone_6,
                                       owner=self.user)
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, self.user.first_name)
        self.assertContains(get_response, self.user.last_name)
        star_reviews = ("<i class=\"material-icons left checked\">grade</i>\n                \n"
                        "                ")
        self.assertContains(get_response, star_reviews*4)
        self.assertNotContains(get_response, star_reviews*5)
        self.assertContains(get_response, "Good job guys")
        self.assertContains(get_response, review.time.strftime("%b."))

    def test_main_image_photos_rendered(self):
        '''
        Test that when you visit a page for a profile which has been added images
        - That the page renders the main image
        - That the page renders other images
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "test_image_5")

    def test_main_image_lack(self):
        '''
        Test that when you visit a page for a profile which has photos and no main images
        - That the page renders the other images with no errors raised
        '''
        PhoneImage.objects.create(phone=self.samsung_j_7, image=image("test_image_7.png"))
        get_response = self.client.get("/profile/{}/".format(self.samsung_j_7.id))
        self.assertContains(get_response, "test_image_7")
        self.assertNotContains(get_response, "test_image_5")

    def test_product_information(self):
        '''
        Test that when you visit a page for a profile with product information added
        - That the page renders the product information
        '''
        ProductInformation.objects.create(phone=self.iphone_6, feature="Network", value="GSM")
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "Network")
        self.assertContains(get_response, "GSM")

    def test_phone_title_rendered(self):
        '''
        Test that when you visit a page for the profile:
        - That the phone title is rendered
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "Iphone 6")

    # def test_star_rendering(self):
    #     '''
    #     Test that when you visit a page for the profile:
    #     - That the stars are rendered properly
    #     - That the number of stars is also rendered properly
    #     '''
    #     Review.objects.create(stars=4, comments="Good job guys", phone=self.iphone_6,
    #                           owner=self.user)
    #     get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
    #     star_count = ("<span class=\"fa fa-star checked\"></span>\n                        \n"
    #                   "                        ")
    #     self.assertContains(get_response, star_count*4)
    #     self.assertNotContains(get_response, star_count*5)
    #     self.assertContains(get_response, 4)

    def test_key_features_rendering(self):
        '''
        Test that when you visit a page for the profile that has key features:
        - That the key features are rendered properly
        '''
        Feature.objects.create(phone=self.iphone_6, feature="64 GB Memcard slot")
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "64 GB Memcard slot")

    # price is not dependent on phone selection
    # def test_currency_rendering(self):
    #     '''
    #     Test that when you visit a page for the profile:
    #     - That the currency and price is rendered
    #     '''
    #     get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
    #     self.assertContains(get_response, "V$ 300,000")

    def test_user_image_rendered(self):
        '''
        Test that when you visit a page for the profile:
            - That the user image is rendered
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "/media/phones/test_image_5_")
