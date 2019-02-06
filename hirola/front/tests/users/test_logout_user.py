""" A module for testing the logout functionality of the application """
from front.base_test import BaseTestCase, Client, User


class LogoutViewTest(BaseTestCase):

    def setUp(self):
        super(LogoutViewTest, self).setUp()
        self.flinstones = Client()
        user = User.objects.create_user(
            email='flinstones@example.com',
            password='test',
            first_name='flinstones'
        )
        self.flinstones.force_login(user)

    def test_logout_user(self):
        """
        Test that if a user has logged into a site and the user logs out
            - That his status changes to unauthenticated. 
        """
        after_login_response = self.flinstones.get("/")
        self.assertTrue(after_login_response.context["user"].is_authenticated)
        self.flinstones.post("/logout")
        after_logout_response = self.flinstones.get("/")
        self.assertFalse(
            after_logout_response.context["user"].is_authenticated)

    def test_redirect_to_current_page_with_referer_header(self):
        """
        Test that if a user has logged out of any page on a browser that
        submits the HTTP_REFERER header
            - That he is redirected to the page he is on.
        """
        logout_response = self.flinstones.post("/logout", HTTP_REFERER="/help")
        self.assertRedirects(logout_response, "/help", 302)

    def test_redirect_to_home_page_without_referer_header(self):
        """
        Test that if a user has logged out of any page on a browser that does
        not submit the HTTP_REFERER header
            - That he is redirected to the home page. 
        """
        get_help_response = self.flinstones.get("/help")
        self.assertEqual(get_help_response.request["PATH_INFO"], "/help")
        logout_response = self.flinstones.post("/logout")
        self.assertRedirects(logout_response, "/", 302)

    def test_user_name_disappears(self):
        """
        Test that if a user has logged out of any page
            - That the page he is redirected to does not contain his first
            name
        """
        after_login_response = self.flinstones.get("/")
        self.assertContains(after_login_response, 'flinstones')
        self.flinstones.post("/logout")
        after_logout_response = self.flinstones.get("/")
        self.assertNotContains(after_logout_response, 'flinstones')
