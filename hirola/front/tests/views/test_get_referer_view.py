""" A module that tests the functionality for the get_referer_view method """
from django.test import RequestFactory
from front.base_test import BaseTestCase
from front.views import get_referer_view


class GetReferViewTest(BaseTestCase):

    def setUp(self):
        super(GetReferViewTest, self).setUp()

    def test_method_returns_home_page_without_referer(self):
        """
        Test that when you call the get_refer_view method without the
        HTTP_REFERER header:
            - That it returns the homepage view
        """
        self.factory = RequestFactory()
        request = self.factory.get('/help')
        referer = get_referer_view(request)
        self.assertEqual(referer, "/")

    def test_method_returns_current_page_with_referer(self):
        """
        Test that when you call the get_refer_view method with the
        HTTP_REFERER header:
            - That it returns the page on the HTTP_REFERER header
        """
        self.factory = RequestFactory()
        request = self.factory.get('/help')
        request.META['HTTP_REFERER'] = '/help'
        referer = get_referer_view(request)
        self.assertEqual(referer, "/help")
