from front.base_test import BaseTestCase, User, Client
from front.forms.user_forms import AuthenticationForm, ChangeEmailForm
from django.core.validators import EmailValidator
from django.utils import timezone


class ConfirmUserView(BaseTestCase):

    def setUp(self):
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.sivanna = Client()
        super(ConfirmUserView, self).setUp()

    def test_login_required_for_confirm_user(self):
        '''
        Test that when a user is not logged in:
            - That he or she cannot access the confirm_user page link
        Test that when a user is logged in:
            - That he can access the confirm_user page link
        '''
        response = self.sivanna.get("/confirm_user")
        self.assertRedirects(response, "/login?next=/confirm_user", 302)

    def test_logged_in_access_confirm_user(self):
        '''
        Test that when a user is logged in:
            - That he can access the confirm_user page link
        '''
        self.sivanna.force_login(self.user)
        response = self.sivanna.get("/confirm_user")
        self.assertEqual(response.status_code, 200)

    def test_wrong_email_format(self):
        '''
        Test that when a wrong email format is granted:
            - That the page does not redirect.
            - That an error message is raised.
        '''
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/confirm_user", {"email": "pop@gmail", "password": "secret"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EmailValidator.message)

    def test_non_existent_email(self):
        '''
        Test that when a valid email format is entered but it does not exist that
            - The page does not redirect.
            - An error message is raised
        '''
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/confirm_user", {"email": "pop@gmail.com",
                                                       "password": "secret"})
        self.assertEqual(response.status_code, 200)
        error_message = AuthenticationForm().error_messages['invalid_email']
        self.assertContains(response, error_message)

    def test_wrong_password(self):
        '''
        Test that when a valid email is entered with a wrong password that
            - The page does not redirect.
            - An error message is raised.
        '''
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/confirm_user", {"email": "sivanna@gmail.com",
                                                       "password": "wrongsecret"})
        self.assertEqual(response.status_code, 200)
        error_message = AuthenticationForm().error_messages['invalid_login']
        self.assertContains(response, error_message)

    def test_valid_credentials(self):
        '''
        Test that when valid credentials are granted to the view:
            - That the page redirects
            - The the user's attribute 'is_change_allowed' changes to true
        '''
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/confirm_user", {"email": "sivanna@gmail.com",
                                                       "password": "secret"})
        self.assertRedirects(response, "/change_email", 302)
        user = User.objects.get(email="sivanna@gmail.com")
        self.assertEqual(user.is_change_allowed, True)


class ChangeEmailView(BaseTestCase):

    def setUp(self):
        super(ChangeEmailView, self).setUp()

    def test_not_logged_in(self):
        '''
        Test that when a user is not logged in:
            - That he is redirected to a log in page
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.sivanna = Client()
        response = self.sivanna.get("/change_email")
        self.assertRedirects(response, "/login?next=/change_email", 302)

    def test_change_allowed_false(self):
        '''
        Test that when a user is logged in and change allowed is False:
            - That the user is redirected to the confirm_user page
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        response = self.sivanna.get("/change_email")
        self.assertRedirects(response, "/confirm_user", 302)

    def test_logged_in_change_allowed_true(self):
        '''
        Test that when a user is logged in and that change allowed is True:
            - That the user can view the page
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.user.is_change_allowed = True
        self.user.save()
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        response = self.sivanna.get("/change_email")
        self.assertEqual(response.status_code, 200)

    def test_wrong_email_format(self):
        '''
        Test that when an invalid email format is provided:
            - That an error is raised
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.user.is_change_allowed = True
        self.user.save()
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/change_email", {"email": "pop@gmail"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EmailValidator.message)

    def test_existent_email(self):
        '''
        Test that when an existent email is provided:
            - That an error is raised
        '''
        # create another user with some credentials for testing
        User.objects.create_user(email="tripona@gmail.com", password="secret")
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.user.is_change_allowed = True
        self.user.save()
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/change_email", {"email": "tripona@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The email address you entered has already been registered.")
        message = "Please provide new email for sivanna@gmail.com"
        self.assertContains(response, message)

    def test_similar_email(self):
        '''
        Test that when a similar email to the user's original email is provided as a candidate
        for change:
            - That an error is raised
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.user.is_change_allowed = True
        self.user.save()
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        response = self.sivanna.post("/change_email", {"email": "sivanna@gmail.com"})
        self.assertEqual(response.status_code, 200)
        error_message = ChangeEmailForm.error_messages['invalid_email']
        self.assertContains(response, error_message)
        message = "Please provide new email for sivanna@gmail.com"
        self.assertContains(response, message)

    def test_valid_data(self):
        '''
        Test that when a valid email is provided that:
            - The users change_allowed attribute is set to False, change_email is set to the
            intended email, change_email_tracker to a time
            - That the status code is 200
            - That a html with information is rendered
        '''
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        self.user = User.objects.get(email="sivanna@gmail.com")
        self.user.is_change_allowed = True
        self.user.save()
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        self.assertIsNone(self.user.change_email_tracker)
        response = self.sivanna.post("/change_email", {"email": "pinotico@gmail.com"})
        self.assertEqual(response.status_code, 200)
        edited_user = User.objects.get(email="sivanna@gmail.com")
        self.assertFalse(edited_user.is_change_allowed)
        self.assertEqual(edited_user.change_email, "pinotico@gmail.com")
        self.assertIsNotNone(edited_user.change_email_tracker)
        msg = "We have sent a link to your new email: "\
              "<b>pinotico@gmail.com</b>"
        self.assertContains(response, "{}".format(msg))
