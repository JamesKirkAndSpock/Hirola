from front.base_test import *
from front.forms.user_forms import FacebookUserForm, FacebookEmailEntryForm
from django.test import RequestFactory
from front.views import facebook_signup_logic, check_email_input, check_facebook_user_id_exists, check_email_update
# from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from importlib import import_module
from django.contrib.auth.models import AnonymousUser


class FacebookUserSignup(BaseTestCase):

    def setUp(self):
        SocialMedia.objects.create(name="instagram", url_link="https://instagram.com",
                            icon="empty")
        SocialMedia.objects.create(name="facebook", url_link="https://facebook.com", icon="empty")
        SocialMedia.objects.create(name="twitter", url_link="https://twitter.com", icon="empty")
        super(FacebookUserSignup, self).setUp()

    def test_facebook_signup_get_request_shows_error(self):
        '''
        Test that when a user visits the url "/facebook_signup" using a GET request, rather than
        with the intention of posting data (POST request):
            - That he gets a view that renders him an error message
        '''
        get_response = self.client.get("/facebook_signup")
        self.assertContains(get_response, "Facebook Error Page")

    def test_facebook_user_form_validity_without_email(self):
        '''
        Test that when a user provides the FacebookUserForm() class with data that omits an email
        address:
            - That validity of the form remains True.
        '''
        data = {"first_name":"dasichi", "last_name":"iutona", "facebook_id":123456}
        form = FacebookUserForm(data)
        self.assertTrue(form.is_valid())


    def test_facebook_user_form_validity_without_id(self):
        '''
        Test that when a user provides the FacebookUserForm() class with data that omits a facebook
        id:
            - That validity of the form id False.
        '''
        data = {"first_name":"dasichi", "last_name":"iutona"}
        form = FacebookUserForm(data)
        self.assertFalse(form.is_valid())

    def test_facebook_signup_without_id(self):
        '''
        Test that when data is provided to the facebook_signup method that does not contain the
        facebook_id of the user:
            - That the page does not redirect
            - That an error is raised on the signup page, that explains there was an error fetching
            data for the user's facebook account.
            - That the page renders phone categories and social media
        '''
        data = {"first_name":"dasichi", "last_name":"iutona"}
        post_response = self.client.post("/facebook_signup", data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "There was an error signing you up using Facebook")
        self.assertContains(post_response, "Iphone")
        self.assertContains(post_response, "Android")
        self.assertContains(post_response, "Tablet")
        self.assertContains(post_response, "Buy Iphone")
        self.assertContains(post_response, "Buy Android")
        self.assertContains(post_response, "Buy Tablet")
        self.assertContains(post_response, "instagram")
        self.assertContains(post_response, "facebook")
        self.assertContains(post_response, "twitter")

    def test_footer_navbar_objects_on_facebook_error_page(self):
        '''
        Test that when a user makes a GET request to the "/facebook_signup" URL:
            - That the view renders phone categories on the navbar
            - That the view renders social media links on the footer
            - That the view renders phone categories on the footer
        '''
        get_response = self.client.get("/facebook_signup")
        self.assertContains(get_response, "Iphone")
        self.assertContains(get_response, "Android")
        self.assertContains(get_response, "Tablet")
        self.assertContains(get_response, "Buy Iphone")
        self.assertContains(get_response, "Buy Android")
        self.assertContains(get_response, "Buy Tablet")
        self.assertContains(get_response, "instagram")
        self.assertContains(get_response, "facebook")
        self.assertContains(get_response, "twitter")

    def test_user_data_saved_with_id_facebook_signup_logic(self):
        '''
        Test that when user data is submitted to the facebook_signup_logic method that:
            - the data is saved regardless of missing some key data like first_name, last_name and
            email or having all the key attributes.
        '''
        self.factory = RequestFactory()
        all_fb_data = {"email": "pop@gmail.com", "first_name":"dasichi",
                        "last_name":"iutona", "facebook_id":123456}
        missing_email_fb_data = {"first_name":"rimond", "last_name":"natuli",
                                 "facebook_id":123457}
        missing_first_name_fb_data = {"last_name":"nikira", "email": "nikira@gmail.com",
                                      "facebook_id":123458}
        missing_last_name_fb_data = {"first_name":"nakusa", "email": "nakusa@gmail.com",
                                      "facebook_id":123459}
        data = [all_fb_data, missing_email_fb_data, missing_first_name_fb_data, missing_last_name_fb_data]
        for item_data in data:
            data_request = self.factory.post('/facebook_signup', data=item_data)
            engine = import_module(settings.SESSION_ENGINE)
            data_request.session = engine.SessionStore()
            data_request.session.save()
            data_request.COOKIES[settings.SESSION_COOKIE_NAME] = data_request.session.session_key
            facebook_signup_logic(data_request)
            user = User.objects.get(facebook_id=item_data.get("facebook_id"))
            self.assertEqual(user.first_name, item_data.get("first_name") or '')
            self.assertEqual(user.last_name, item_data.get("last_name") or '')
            self.assertEqual(user.email, item_data.get("email") or '')

    def test_email_redirection_facebook_signup_logic(self):
        '''
        Test that when user data is submitted to the facebook_signup_logic with or without user
        email that:
            - when the data has an email the user is redirected to the dashboard
            - when the data has no email the user is redirected to the facebook_email_signup url
        '''
        self.factory = RequestFactory()
        all_fb_data = {"email": "pop@gmail.com", "first_name":"dasichi",
                        "last_name":"iutona", "facebook_id":123456}
        missing_email_fb_data = {"first_name":"rimond", "last_name":"natuli",
                                 "facebook_id":123457}
        missing_first_name_fb_data = {"last_name":"nikira", "email": "nikira@gmail.com",
                                      "facebook_id":123458}
        missing_last_name_fb_data = {"first_name":"nakusa", "email": "nakusa@gmail.com",
                                      "facebook_id":123459}
        data = [all_fb_data, missing_email_fb_data, missing_first_name_fb_data, missing_last_name_fb_data]
        for item_data in data:
            data_request = self.factory.post('/facebook_signup', data=item_data)
            engine = import_module(settings.SESSION_ENGINE)
            data_request.session = engine.SessionStore()
            data_request.session.save()
            data_request.COOKIES[settings.SESSION_COOKIE_NAME] = data_request.session.session_key
            response = facebook_signup_logic(data_request)
            if item_data.get("email"):
                self.assertEqual(response.url, "/dashboard")
            else:
                self.assertEqual(response.url, "/facebook_email_signup")

    def test_get_facebook_email_signup(self):
        '''
        Test that when a user gets the facebook email signup page:
            - That the response is a 200.
            - That he gets a page with words 'Please provide your email address to finish your
            signup' 
        '''
        response = self.client.get("/facebook_email_signup")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please provide your email address to finish your signup")

    def test_check_email_input(self):
        '''
        Test that the check_email_input method will
            - return dashboard page when given an email and the user is logged in
            - return facebook_email_signup when not given an email
        '''
        self.factory = RequestFactory()
        no_email_post_request = self.factory.post("/facebook_signup", {"":""})
        emtpy_email_response = check_email_input(no_email_post_request)
        self.assertEqual(emtpy_email_response.status_code, 302)
        self.assertEqual(emtpy_email_response.url, "/facebook_email_signup")
        email_post_request = self.factory.post("/facebook_signup", {"email":"example@gmail.com", "facebook_id": 1234})
        engine = import_module(settings.SESSION_ENGINE)
        email_post_request.session = engine.SessionStore()
        email_post_request.session.save()
        email_post_request.COOKIES[settings.SESSION_COOKIE_NAME] = email_post_request.session.session_key
        User.objects.create(email="pinocchio@gmail.com")
        get_user = User.objects.get(email="pinocchio@gmail.com")
        email_post_request.user = get_user
        email_response = check_email_input(email_post_request)
        self.assertEqual(email_response.status_code, 302)
        self.assertEqual(email_response.url, "/dashboard")

    def test_valid_email_on_facebook_email_entry_form(self):
        '''
        Test that when you submit valid data to the FacebookEmailEntryForm:
            - that the form will be regarded as valid
        '''
        valid_data = {"email": "example@gmail.com"}
        form = FacebookEmailEntryForm(valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_on_facebook_email_entry_form(self):
        '''
        Test that when you submit invalid data to the FacebookEmailEntryForm:
            - that the form will be regarded as invalid
        '''
        invalid_email_data = {"email": "example@gmail"}
        form = FacebookEmailEntryForm(invalid_email_data)
        self.assertIn("Enter a valid email address.", form.errors.get("email"))
        self.assertFalse(form.is_valid())

    def test_existent_email_on_facebook_email_entry_form(self):
        '''
        Test that when you submit existent email to the FacebookEmailEntryForm:
            - that the form will be regarded as invalid
        '''
        User.objects.create_user(email="example@gmail.com")
        existent_email_data = {"email": "example@gmail.com"}
        form = FacebookEmailEntryForm(existent_email_data)
        self.assertIn("The email address you entered has already been registered.",
                      form.errors.get("email"))
        self.assertIn(FacebookEmailEntryForm().error_messages["unique_forgot_password_message"], form.errors.get("email"))
        self.assertIn(FacebookEmailEntryForm().error_messages["unique_login_message"], form.errors.get("email"))
        self.assertFalse(form.is_valid())

    def test_post_data_facebook_email_signup_valid_email(self):
        '''
        Test that when you submit a valid email to the facebook_email_signup page:
            - that the page will redirect
            - that the email data will be saved.
        '''
        valid_email_data = {"email": "example@gmail.com"}
        valid_email_data_response = self.client.post('/facebook_email_signup', data=valid_email_data)
        self.assertEqual(valid_email_data_response.status_code, 302)
        self.assertEqual(valid_email_data_response.url, "/dashboard")
        self.assertTrue(User.objects.filter(email="example@gmail.com").first())

    def test_post_data_facebook_email_signup_invalid_email(self):
        '''
        Test that posting an email that is invalid on the facebook_email_signup page:
            - will not redirect the page
            - will render an email error that will inform him the email is invalid.
        '''
        invalid_email_data = {"email": "example@gmail"}
        invalid_email_data_response = self.client.post('/facebook_email_signup', data=invalid_email_data)
        self.assertEqual(invalid_email_data_response.status_code, 200)
        self.assertFalse(User.objects.filter(email="example@gmail.com").first())
        self.assertContains(invalid_email_data_response, "Enter a valid email address.")

    def test_post_data_facebook_email_signup_existent_email(self):
        '''
        Test that posting an email that is invalid on the facebook_email_signup page:
            - will not redirect the page
            - will render an email error that will advise the user to login without facebook.
        '''
        User.objects.create_user(email="example@gmail.com")
        existent_email_data = {"email": "example@gmail.com"}
        existent_email_data_response = self.client.post('/facebook_email_signup', data=existent_email_data)
        self.assertEqual(existent_email_data_response.status_code, 200)
        existent_email_error = "The email address you entered has already been registered."
        self.assertContains(existent_email_data_response, existent_email_error)
        self.assertContains(existent_email_data_response, 
                            FacebookEmailEntryForm().error_messages["unique_forgot_password_message"])
        self.assertContains(existent_email_data_response, 
                            FacebookEmailEntryForm().error_messages["unique_login_message"])

    def test_check_facebook_user_id_exists_user_already_exists(self):
        '''
        Test that if a facebook user had already signed up to the site before:
            - That the check_facebook_user_id_exists will redirect the user to the dashboard page
            - That the check_facebook_user_id_exists will log the user in
        '''
        User.objects.create_user(email="example@gmail.com", facebook_id=123456)
        user_data = {"email": "example@gmail.com", "first_name":"dasichi", "last_name":"iutona", "facebook_id":123456}
        before_login_user = User.objects.get(email="example@gmail.com")
        self.assertFalse(before_login_user.last_login)
        self.factory = RequestFactory()
        data_request = self.factory.post('/facebook_signup', data=user_data)
        engine = import_module(settings.SESSION_ENGINE)
        data_request.session = engine.SessionStore()
        data_request.session.save()
        data_request.COOKIES[settings.SESSION_COOKIE_NAME] = data_request.session.session_key
        response = check_facebook_user_id_exists(data_request)
        self.assertEqual(response.url, "/dashboard")
        self.assertEqual(response.status_code, 302)
        after_login_user = User.objects.get(email="example@gmail.com")
        self.assertTrue(after_login_user.last_login)

    def test_check_email_update_new_email(self):
        '''
        Test that if a user had signed up with facebook before and he or she changed her email
        before logging in again with facebook:
            - That the email address is updated for the user.
            - That the former email is added to the former_email attribute of a user
        '''
        User.objects.create_user(email="example@gmail.com", facebook_id=123456)
        facebook_user = User.objects.get(facebook_id=123456)
        user_data = {"email": "pop@gmail.com", "first_name":"dasichi", "last_name":"iutona", "facebook_id":123456}
        self.factory = RequestFactory()
        data_request = self.factory.post('/facebook_signup', data=user_data)
        engine = import_module(settings.SESSION_ENGINE)
        data_request.session = engine.SessionStore()
        data_request.session.save()
        data_request.COOKIES[settings.SESSION_COOKIE_NAME] = data_request.session.session_key
        response = check_email_update(data_request, facebook_user)
        after_email_check_facebook_user = User.objects.get(facebook_id=123456)
        self.assertEqual(after_email_check_facebook_user.former_email, "example@gmail.com")
        self.assertEqual(after_email_check_facebook_user.email, "pop@gmail.com")

    def test_check_email_update_no_new_email(self):
        User.objects.create_user(email="example@gmail.com", facebook_id=123456)
        facebook_user = User.objects.get(facebook_id=123456)
        user_data = {"email": "example@gmail.com", "first_name":"dasichi", "last_name":"iutona", "facebook_id":123456}
        self.factory = RequestFactory()
        data_request = self.factory.post('/facebook_signup', data=user_data)
        engine = import_module(settings.SESSION_ENGINE)
        data_request.session = engine.SessionStore()
        data_request.session.save()
        data_request.COOKIES[settings.SESSION_COOKIE_NAME] = data_request.session.session_key
        response = check_email_update(data_request, facebook_user)
        after_email_check_facebook_user = User.objects.get(facebook_id=123456)
        self.assertEqual(after_email_check_facebook_user.former_email, None)
        self.assertEqual(after_email_check_facebook_user.email, "example@gmail.com")

    def test_error_non_existent_on_successful_signup(self):
        valid_email_data = {"email": "example@gmail.com"}
        valid_email_data_response = self.client.post('/facebook_email_signup', data=valid_email_data, follow=True)
        self.assertNotContains(valid_email_data_response, "There was an error signing you up using Facebook")
