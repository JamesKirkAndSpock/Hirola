""" A module for testing the login functionality of the application """
from front.base_test import BaseTestCase, Client, User


class LoginViewTest(BaseTestCase):

    def setUp(self):
        super(LoginViewTest, self).setUp()
        self.bed_rock = Client()
        User.objects.create(
            email="timonpumba@gmail.com", first_name="timon",
            last_name="pumba", is_staff=True, is_active=True,
            is_change_allowed=False,
            country_code=self.code,
            phone_number=722000000
            )
        self.timon = User.objects.get(email="timonpumba@gmail.com")
        self.timon.set_password("secret")
        self.timon.save()

    def test_next_on_login(self):
        """
        Test that if a user visits the login page with the next on
        the variable on the URL
            - That a successful login redirects to the URL specified
            on the next variable
        """
        login_data = {"email": "timonpumba@gmail.com", "password": "secret"}
        response = self.bed_rock.post("/login?next=/dashboard", login_data)
        self.assertRedirects(response, "/dashboard")
