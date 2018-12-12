from front.base_test import *
from unittest.mock import Mock
from front.decorators import is_change_allowed_required, old_password_required, remember_user
from django.test import RequestFactory
from django.conf import settings


class DecoratorsTest(BaseTestCase):

    def setUp(self):
        User.objects.create(email="sivanna@gmail.com", first_name="Sivanna", last_name="Turimo",
                            is_staff=False, is_active=True, is_change_allowed=False,
                            phone_number=718217411, )
        self.user = User.objects.get(first_name="Sivanna")
        self.sivanna = Client()
        self.sivanna.force_login(self.user)
        self.function = Mock()
        self.request = RequestFactory()
        self.request.user = self.user
        super(DecoratorsTest, self).setUp()

    def test_is_change_allowed_decorator_false(self):
        '''
        Test that when a mock function and a request with a user whose 'is_change_allowed' attribute
        is set to False is granted to a decorator function that:
            - The response redirects to the confirm user page
        '''
        self.assertEqual(self.request.user.is_change_allowed, False)
        decorator = is_change_allowed_required(self.function)
        response = decorator(self.request)
        response.client = self.sivanna
        self.assertRedirects(response, "/confirm_user", 302)

    def test_is_change_allowed_decorator_true(self):
        '''
        Test that when a mock function and a request with a user whose 'is_change_allowed' attribute
        is set to True is granted to a decorator function that:
            - The response returns the mock function provided
        '''
        request = self.request
        request.user.is_change_allowed = True
        self.assertEqual(self.request.user.is_change_allowed, True)
        decorator = is_change_allowed_required(self.function)
        response = decorator(request)
        self.assertEqual(isinstance(response, Mock), True)

    def test_old_password_required_decorator_false(self):
        '''
        Test that when a mock function and a request with a user whose 'is_change_allowed' attribute
        is set to False is granted to a decorator function that:
            - The response redirects to the confirm user page
        '''
        self.assertEqual(self.request.user.is_change_allowed, False)
        decorator = old_password_required(self.function)
        response = decorator(self.request)
        response.client = self.sivanna
        self.assertRedirects(response, "/old_password", 302)

    def test_old_password_required_decorator_true(self):
        '''
        Test that when a mock function and a request with a user whose 'is_change_allowed' attribute
        is set to True is granted to a decorator function that:
            - The response returns the mock function provided
        '''
        request = self.request
        request.user.is_change_allowed = True
        self.assertEqual(self.request.user.is_change_allowed, True)
        decorator = old_password_required(self.function)
        response = decorator(request)
        self.assertEqual(isinstance(response, Mock), True)
