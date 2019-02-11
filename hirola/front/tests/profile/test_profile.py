from front.base_test import *


class PhoneProfileLogic(BaseTestCase):
    '''
    Test functionality on the backend that occurs on the phone profile page
    '''
    def setUp(self):
        User.objects.create(email="example@gmail.com", first_name="Example",
                            last_name="User", is_staff=False, is_active=True,
                            is_change_allowed=False, phone_number=72200000, )
        self.user = User.objects.get(first_name="Example")
        super(PhoneProfileLogic, self).setUp()
        Review.objects.create(stars=4, comments="Good job guys",
                              phone=self.iphone_6, owner=self.user)
        Review.objects.create(stars=2, comments="You can improve",
                              phone=self.iphone_6, owner=self.user)
        Review.objects.create(stars=5, comments="Awesome job",
                              phone=self.iphone_6, owner=self.user)

    def test_stars_addition(self):
        '''
        Test that when a customer review is added:
        - that the average is calculated accurately
        '''
        get_response = self.client.get("/profile/{}/".
                                       format(self.iphone_6.id))
        star_count = ("\n                                \n"
                      "                                "
                      "<span class=\"fa fa-star checked\"></span>")
        unchecked_star_count = ("<span class=\"fa fa-star\">"
                                "</span>\n                                \n"
                                "                                ")
        self.assertContains(get_response, star_count*4)
        self.assertContains(get_response, unchecked_star_count)
        self.assertNotContains(get_response, star_count*5)
        self.assertContains(get_response, 4)
        Review.objects.create(stars=1, comments="Awesome job",
                              phone=self.iphone_6, owner=self.user)
        Review.objects.create(stars=2, comments="Awesome job",
                              phone=self.iphone_6, owner=self.user)
        get_response_2 = self.client.get("/profile/{}/".
                                         format(self.iphone_6.id))
        self.assertContains(get_response_2, star_count*3)
        self.assertContains(get_response_2, unchecked_star_count*2)
        self.assertNotContains(get_response_2, star_count*4)
        self.assertContains(get_response_2, 3)

    def test_stars_removal(self):
        '''
        Test that when a customer review is removed:
        - that the average is calculated accurately
        '''
        get_response = self.client.get("/profile/{}/".
                                       format(self.iphone_6.id))
        star_count = ("\n                                \n"
                      "                                "
                      "<span class=\"fa fa-star checked\"></span>")
        unchecked_star_count = ("<span class=\"fa fa-star\">"
                                "</span>\n                                \n"
                                "                                ")
        self.assertContains(get_response, star_count*4)
        self.assertContains(get_response, unchecked_star_count)
        self.assertNotContains(get_response, star_count*5)
        review = Review.objects.get(comments="You can improve")
        review.delete()
        get_response_2 = self.client.get("/profile/{}/".
                                         format(self.iphone_6.id))
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