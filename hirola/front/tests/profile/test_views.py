"""Contains tests for profile views."""
from front.base_test import (BaseTestCase, User, image)
from front.models import (ProductInformation, Review, Feature)


class PhoneProfileTemplate(BaseTestCase):
    '''
    Test that templates render the correct information due to objects added on
    the database
    '''
    def setUp(self):
        User.objects.create(email="example@gmail.com", first_name="Example",
                            last_name="User", is_staff=False, is_active=True,
                            is_change_allowed=False, phone_number=72200000,
                            photo=image("test_image_5.png"))
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
        review = Review.objects.create(
            stars=4, comments="Good job guys",
            phone_model=self.samsung_note_5, owner=self.user
            )
        get_response = self.client.get(
            "/profile/{}/".format(self.samsung_note_5.id)
            )
        self.assertContains(get_response, self.user.first_name)
        self.assertContains(get_response, self.user.last_name)
        star_reviews = ("<i class=\"material-icons left checked\">grade</i>\n"
                        "                \n                ")
        self.assertContains(get_response, star_reviews*4)
        self.assertNotContains(get_response, star_reviews*5)
        self.assertContains(get_response, "Good job guys")
        self.assertContains(get_response, review.time.strftime("%b"))

    def test_main_image_photos_rendered(self):
        '''
        Test that when you visit a page for a profile which has been
            added images
        - That the page renders the main image
        - That the page renders other images
        '''
        get_response = self.client.get(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.id)
            )
        self.assertContains(get_response, "test_image_5")

    def test_product_information(self):
        '''
        Test that when you visit a page for a profile with product
            information added
        - That the page renders the product information
        '''
        ProductInformation.objects.create(phone=self.samsung_note_5_rose_gold,
                                          feature="Network", value="GSM")
        get_response = self.client.get(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.id)
            )
        self.assertContains(get_response, "Network")
        self.assertContains(get_response, "GSM")

    def test_phone_title_rendered(self):
        '''
        Test that when you visit a page for the profile:
        - That the phone title is rendered
        '''
        get_response = self.client.get("/profile/{}/".
                                       format(self.samsung_note_5.id))
        self.assertContains(get_response, "Samsung Note 5")

    def test_star_rendering(self):
        '''
        Test that when you visit a page for the profile:
        - That the stars are rendered properly
        - That the number of stars is also rendered properly
        '''
        Review.objects.create(
            stars=4, comments="Good job guys",
            phone_model=self.samsung_note_5, owner=self.user
            )
        get_response = self.client.get("/profile/{}/".
                                       format(self.samsung_note_5.id))
        star_count = ("\n                                \n"
                      "                                "
                      "<span class=\"fa fa-star checked\"></span>")
        self.assertContains(get_response, star_count*4)
        self.assertNotContains(get_response, star_count*5)
        self.assertContains(get_response, 4)

    def test_key_features_rendering(self):
        '''
        Test that when you visit a page for the profile that has key features:
        - That the key features are rendered properly
        '''
        Feature.objects.create(phone=self.samsung_note_5_rose_gold,
                               feature="64 GB Memcard slot")
        get_response = self.client.get(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.id)
            )
        self.assertContains(get_response, "64 GB Memcard slot")

    def test_user_image_rendered(self):
        '''
        Test that when you visit a page for the profile:
            - That the user image is rendered
        '''
        get_response = self.client.get(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.id)
            )
        self.assertContains(get_response, "/media/phones/test_image_5_")
