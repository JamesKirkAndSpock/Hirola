from front.base_test import *
from front.tests.test_users import UserSignupTestCase

class DashboardLogic(BaseTestCase):

    def setUp(self):
        super(DashboardLogic, self).setUp()
        user_data = UserSignupTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        html_content = "To activate this email, you need to click on the activation link that was sent on this email"
        self.assertContains(response, html_content)
        self.uriel = Client()
        user = User.objects.get(email="urieltimanko@example.com")
        user.is_active = True
        user.save()
        self.uriel.force_login(user)

    def test_name_edition(self):
        '''
        Test that when a logged in user edits his first and last name by
        entering the data correctly that:
            - The user remains on the dashboard page.
            - The first name is changed properly
            - The last name is changed properly
        '''
        first_name_data = {"first_name": "Britney"}
        response = self.uriel.post('/dashboard', first_name_data)
        self.assertEqual(response.status_code, 200)
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, "Britney")
        last_name_data = {"last_name": "Delila"}
        response = self.uriel.post('/dashboard', last_name_data)
        self.assertEqual(response.status_code, 200)
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, "Delila")

    def test_contact_edition(self):
        '''
        Test that when a logged in user edits his country code and phone number
        by entering the data correctly that:
            - The user remains on the dashboard page.
            - The country code is changed properly
            - The last name is changed properly
        '''
        CountryCode.objects.create(country_code=256, country="Uganda")
        country_code = CountryCode.objects.filter(country_code=256).first()
        country_code_data = {"country_code": country_code.id}
        response = self.uriel.post('/dashboard', country_code_data)
        self.assertEqual(response.status_code, 200)
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, str(country_code))
        phone_data = {"phone_number": 220000}
        response = self.uriel.post('/dashboard', phone_data)
        self.assertEqual(response.status_code, 200)
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, 220000)

    def test_old_password_validation(self):
        '''
        Test that when a user enters the wrong old password:
            - The user remains on the same page and is not redirected.
            - The user is prompted with an error message
        Test that when a user enters the correct old password:
            - The user is redirected to a page to edit the password
        '''
        response = self.uriel.post('/old_password', {"old_password": "wrong_password"})
        self.assertEqual(response.status_code, 200)
        error_message = "Your old password was entered incorrectly. Please enter it again."
        self.assertContains(response, error_message)
        response_1 = self.uriel.post('/old_password', {"old_password": "*&#@&!*($)lp"})
        self.assertRedirects(response_1, "/change_password", 302)

    def test_view_login_required(self):
        '''
        Test that if a user has not been logged in that:
            - He cannot access the dashboard view.
            - He cannot access the old password view.
            - He cannot access the change password view.
            - He is redirected to the login view
        '''
        old_password_view = self.client.get("/old_password")
        self.assertRedirects(old_password_view, "/login?next=/old_password", 302)
        dashboard_view = self.client.get('/dashboard')
        self.assertRedirects(dashboard_view, "/login?next=/dashboard", 302)
        change_password_view = self.client.get('/change_password')
        self.assertRedirects(change_password_view, "/login?next=/change_password", 302)

    def test_change_password_old_password_validation(self):
        '''
        Test that when a logged in user manually goes to the change_password
        view that:
            - He cannot access the view
            - He is redirected to the old_password view inorder to insert his
            old password.
        '''
        change_password_view = self.uriel.get('/change_password')
        self.assertRedirects(change_password_view, "/old_password", 302)

    def test_change_password(self):
        '''
        Test that when a user is changing a password that:
            - He is redirected to the login page
        '''
        self.uriel.post('/old_password', {"old_password": "*&#@&!*($)lp"})
        response = self.uriel.post('/change_password', {"new_password1": "!@£$!@£$!@£$£!@$!@£$!@3",
                                   "new_password2": "!@£$!@£$!@£$£!@$!@£$!@3"})
        self.assertRedirects(response, "/login", 302)
