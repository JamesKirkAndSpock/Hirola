from front.base_test import *
from front.tests.test_users import UserSignupTestCase
from django.contrib.humanize.templatetags.humanize import naturaltime


class PhoneProfileTemplate(BaseTestCase):
    '''
    Test that templates render the correct information due to objects added on
    the database
    '''
    def setUp(self):
        User.objects.create(email="example@gmail.com", first_name="Example",
                            last_name="User", is_staff=False, is_active=True,
                            is_change_allowed=False, phone_number=718217411, )
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

    def test_star_rendering(self):
        '''
        Test that when you visit a page for the profile:
        - That the stars are rendered properly
        - That the number of stars is also rendered properly
        '''
        Review.objects.create(stars=4, comments="Good job guys", phone=self.iphone_6,
                              owner=self.user)
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        star_count = ("<span class=\"fa fa-star checked\"></span>\n                        \n"
                      "                        ")
        self.assertContains(get_response, star_count*4)
        self.assertNotContains(get_response, star_count*5)
        self.assertContains(get_response, 4)

    def test_key_features_rendering(self):
        '''
        Test that when you visit a page for the profile that has key features:
        - That the key features are rendered properly
        '''
        Feature.objects.create(phone=self.iphone_6, feature="64 GB Memcard slot")
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "64 GB Memcard slot")

    def test_currency_rendering(self):
        '''
        Test that when you visit a page for the profile:
        - That the currency and price is rendered
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response, "V$ 300,000")


class PhoneProfileLogic(BaseTestCase):
    '''
    Test functionality on the backend that occurs on the phone profile page
    '''
    def setUp(self):
        User.objects.create(email="example@gmail.com", first_name="Example",
                            last_name="User", is_staff=False, is_active=True,
                            is_change_allowed=False, phone_number=718217411, )
        self.user = User.objects.get(first_name="Example")
        super(PhoneProfileLogic, self).setUp()
        Review.objects.create(stars=4, comments="Good job guys", phone=self.iphone_6,
                              owner=self.user)
        Review.objects.create(stars=2, comments="You can improve", phone=self.iphone_6,
                              owner=self.user)
        Review.objects.create(stars=5, comments="Awesome job", phone=self.iphone_6, owner=self.user)

    def test_stars_addition(self):
        '''
        Test that when a customer review is added:
        - that the average is calculated accurately
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        star_count = ("<span class=\"fa fa-star checked\"></span>\n                        \n"
                      "                        ")
        unchecked_star_count = ("<span class=\"fa fa-star\"></span>\n                        \n"
                                "                        ")
        self.assertContains(get_response, star_count*4)
        self.assertContains(get_response, unchecked_star_count)
        self.assertNotContains(get_response, star_count*5)
        self.assertContains(get_response, 4)
        Review.objects.create(stars=1, comments="Awesome job", phone=self.iphone_6, owner=self.user)
        Review.objects.create(stars=2, comments="Awesome job", phone=self.iphone_6, owner=self.user)
        get_response_2 = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response_2, star_count*3)
        self.assertContains(get_response_2, unchecked_star_count*2)
        self.assertNotContains(get_response_2, star_count*4)
        self.assertContains(get_response_2, 3)

    def test_stars_removal(self):
        '''
        Test that when a customer review is removed:
        - that the average is calculated accurately
        '''
        get_response = self.client.get("/profile/{}/".format(self.iphone_6.id))
        star_count = ("<span class=\"fa fa-star checked\"></span>\n                        \n"
                      "                        ")
        unchecked_star_count = ("<span class=\"fa fa-star\"></span>\n                        \n"
                                "                        ")
        self.assertContains(get_response, star_count*4)
        self.assertContains(get_response, unchecked_star_count)
        self.assertNotContains(get_response, star_count*5)
        review = Review.objects.get(comments="You can improve")
        review.delete()
        get_response_2 = self.client.get("/profile/{}/".format(self.iphone_6.id))
        self.assertContains(get_response_2, star_count*4)
        self.assertContains(get_response_2, unchecked_star_count)
        self.assertNotContains(get_response_2, star_count*5)

    def test_non_existent_phone_profile(self):
        '''
        Test that when a customer looks for a non existent phone profile
            - That he gets a 404 error message
        '''
        response = self.client.get("/profile/123456789/")
        self.assertRedirects(response, "/error", 302)
