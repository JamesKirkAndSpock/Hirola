from front.base_test import *
from front.errors import *


class UserSignupTestCase(BaseTestCase):
    def setUp(self):
        super(UserSignupTestCase, self).setUp()
        data = {"area_code": "254", "country": "Kenya"}
        response = self.elena.post('/admin/front/areacode/add/', data)
        self.area_code = AreaCode.objects.filter(area_code=254).first()

    def test_area_code_creation(self):
        '''
        Test that after the area code is created on setting up tests:
            - The area code was filled in with the right data.
        '''
        self.assertEqual(self.area_code.country, "Kenya")

    def test_successful_creation_of_user(self):
        '''
        Test that when a user serves correct input data to the signup form:
            - The user is added to the database.
            - The user is visible in the admin page.
            - The data was entered correctly.
            - The page redirects currently to the landing page
        '''
        user_data = {"first_name": "Uriel", "last_name": "Timanko",
                     "area_code": self.area_code.id, "phone_number": 722000000,
                     "email": "urieltimanko@example.com",
                     "password1": "*&#@&!*($)lp",
                     "password2": "*&#@&!*($)lp"}
        response = self.client.post('/signup', user_data)
        self.assertRedirects(response, "/", 302)
        user = User.objects.filter(first_name="Uriel").first()
        self.assertEqual(user.last_name, "Timanko")
        self.assertEqual(user.email, "urieltimanko@example.com")
        self.assertEqual(user.phone_number, 722000000)
        self.assertEqual(user.area_code, self.area_code)
        response = self.elena.get("/admin/front/user/")
        self.assertContains(response, "Uriel")

    def test_similar_password_validation(self):
        '''
        Test that when a user is signing up and the Password and Confirm
        Password fields do not match:
            - The signup form does not redirect
            - The user gets an error message tailored to the wrong entry
        '''
        user_data = {"first_name": "Uriel", "last_name": "Timanko",
                     "area_code": self.area_code.id, "phone_number": 722000000,
                     "email": "urieltimanko@example.com",
                     "password1": "*&#@&!*($)lp",
                     "password2": "*&#@&!*($)l"}
        response = self.client.post('/signup', user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "The two password fields didn&#39;t match")

    def test_invalid_number_validation(self):
        '''
        Test that when a user is signing up and inputs an invalid number that:
            - The user is given an error message explaining that the number
            he or she used is invalid.
            - The page does not redirect.
        '''
        user_data = {"first_name": "Uriel", "last_name": "Timanko",
                     "area_code": self.area_code.id,
                     "phone_number": 7220000000,
                     "email": "urieltimanko@example.com",
                     "password1": "*&#@&!*($)lp",
                     "password2": "*&#@&!*($)lp"}
        response = self.client.post('/signup', user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The phone number entered is invalid.")

    def test_password_format_validation(self):
        '''
        Test that when a user is signing up and inputs a password that is not
        in the right format:
            - That the page does not redirect.
            - That the user gets an informative message of the issue with the
            password input.
        '''
        user_data = {"first_name": "Uriel", "last_name": "Timanko",
                     "area_code": self.area_code.id,
                     "phone_number": 722000000,
                     "email": "urieltimanko@example.com",
                     "password1": "pass",
                     "password2": "pass"}
        response = self.client.post('/signup', user_data)
        self.assertContains(response, "This password is too common.")
        error_message = ("This password is too short. It must contain at least"
                         " 8 characters.")
        self.assertContains(response, error_message)

    def test_email_format_validation(self):
        '''
        Test that when a user is signing up and inputs an email that is not in
        the right format:
            - That the page does not redirect.
            - That the user gets and informative message of the issue with the
            email input.
        '''
        user_data = {"first_name": "Uriel", "last_name": "Timanko",
                     "area_code": self.area_code.id, "phone_number": 722000000,
                     "email": "urieltimanko@examplecom",
                     "password1": "*&#@&!*($)lp",
                     "password2": "*&#@&!*($)lp"}
        response = self.client.post('/signup', user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address")
