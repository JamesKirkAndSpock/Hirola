from front.base_test import *
from front.errors import *
from front.forms import AuthenticationForm


class UserSignupTestCase(BaseTestCase):
    def setUp(self):
        super(UserSignupTestCase, self).setUp()

    def test_successful_creation_of_user(self):
        '''
        Test that when a user serves correct input data to the signup form:
            - The user is added to the database.
            - The user is visible in the admin page.
            - The data was entered correctly.
            - The page redirects currently to the landing page
        '''
        user_data = self.generate_user_data({})
        response = self.client.post('/signup', user_data)
        self.assertRedirects(response, "/", 302)
        user = User.objects.filter(first_name="Uriel").first()
        self.assertEqual(user.last_name, "Timanko")
        self.assertEqual(user.email, "urieltimanko@example.com")
        self.assertEqual(user.phone_number, 722000000)
        self.assertEqual(user.area_code.id, user_data["area_code"])
        response = self.elena.get("/admin/front/user/")
        self.assertContains(response, "Uriel")

    def test_similar_password_validation(self):
        '''
        Test that when a user is signing up and the Password and Confirm
        Password fields do not match:
            - The signup form does not redirect
            - The user gets an error message tailored to the wrong entry
        '''
        user_data = self.generate_user_data({"password2": "*&#@&!*($)l"})
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
        user_data = self.generate_user_data({"phone_number": 7220000000})
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
        user_data = self.generate_user_data({"password1": "pass",
                                             "password2": "pass"})
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
            - That the user gets an informative message of the issue with the
            email input.
        '''
        user_data = self.generate_user_data({"email": "urieltimanko@examplecom"})
        response = self.client.post('/signup', user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address")

    def test_email_uniqueness(self):
        '''
        Test that when a user is signing up and inputs an email of a user that
        has already signed up:
            - That the page does not redirect.
            - That the user gets an informative issue that the email is a
            duplicate
        '''
        user_data = self.generate_user_data({})
        response = self.client.post('/signup', user_data)
        self.assertRedirects(response, "/", 302)
        user_2 = self.generate_user_data({"first_name": "Another",
                                          "last_name": "User"})
        response = self.client.post('/signup', user_2)
        self.assertEqual(response.status_code, 200)
        error_message = ('The email address you entered has already been'
                         ' registered.')
        self.assertContains(response, error_message)

    def generate_user_data(self, data):
        '''
        Generate data for a user to be posted to the signup page
        '''
        AreaCode.objects.create(area_code=254, country="Kenya")
        area_code = AreaCode.objects.filter(area_code=254).first()
        user_data = {"first_name": data.get('first_name') or "Uriel",
                     "last_name": data.get('last_name') or "Timanko",
                     "area_code": area_code.id,
                     "phone_number": data.get('phone_number') or 722000000,
                     "email": data.get('email') or "urieltimanko@example.com",
                     "password1": data.get('password1') or "*&#@&!*($)lp",
                     "password2": data.get('password2') or "*&#@&!*($)lp"}
        return user_data


class UserLoginTestCase(BaseTestCase):

    def setUp(self):
        super(UserLoginTestCase, self).setUp()
        user_data = UserSignupTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        self.assertRedirects(response, "/", 302)

    def test_successful_account_creation(self):
        '''
        Test that when a user enters correct data for logging in that:
            - The user is redirected currently to the landing page.
        '''
        user_data = {"email": "urieltimanko@example.com",
                     "password": "*&#@&!*($)lp"}
        response = self.client.post('/login', user_data)
        self.assertRedirects(response, "/", 302)

    def test_wrong_password_input(self):
        '''
        Test that when a user enters correct email but a wrong password that:
            - The page does not redirect.
            - The user gets a descriptive error message explaining that the
            password and email does not match.
        '''
        user_data = {"email": "urieltimanko@example.com",
                     "password": "*&#@&!*($)l"}
        response = self.client.post('/login', user_data)
        self.assertEqual(response.status_code, 200)
        error_message = AuthenticationForm().error_messages["invalid_login"]
        self.assertContains(response, error_message)

    def test_wrong_email_input(self):
        '''
        Test that when a user enters a wrong email but a correct password that:
            - The page does not redirect
            - The user gets a descriptive message explaining that the password
            and email does not match
        '''
        user_data = {"email": "urieltimanko@example.cm",
                     "password": "*&#@&!*($)lp"}
        response = self.client.post('/login', user_data)
        self.assertEqual(response.status_code, 200)
        error_message = AuthenticationForm().error_messages["invalid_login"]
        self.assertContains(response, error_message)

    def test_user_cannot_login_if_inactive(self):
        '''
        Test that when the admin makes the user inactive:
            -  The page does not redirect
            - The user is given a descriptive message that he is an inactive
            user.
        '''
        user = User.objects.get(email="urieltimanko@example.com")
        user.is_active = False
        user.save()
        user_data = {"email": "urieltimanko@example.com",
                     "password": "*&#@&!*($)lp"}
        response = self.client.post('/login', user_data)
        self.assertEqual(response.status_code, 200)
        error_message = AuthenticationForm().error_messages["invalid_login"]
        self.assertContains(response, error_message)
