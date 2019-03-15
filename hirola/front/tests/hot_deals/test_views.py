"""Test the views of a hot_deal"""
from front.base_test import BaseTestCase
from django.test import Client
from front.models import User, Cart, HotDeal


class HotDealsViewsTestCase(BaseTestCase):
    """Tests the hot_deals views"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(HotDealsViewsTestCase, self).setUp()
        HotDeal.objects.create(item=self.samsung_note_5_rose_gold)
        self.hot_deal = HotDeal.objects.get(
            item=self.samsung_note_5_rose_gold)

    def test_hot_deal_view_post_logged_in(self):
        """
        Test that when an identified user makes a post on the hot deal
        view page
            - That the user is redirected to the before_checkout page
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        response = self.winniethepooh.post(
            "/hot_deal/{}/".format(self.hot_deal.pk),
            {'phone_model_item': self.samsung_note_5_rose_gold.pk,
             'quantity': 4, 'owner': '', 'session_key': ''})
        self.assertRedirects(response, "/before_checkout")
        cart = Cart.objects.get(
            owner=user,
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=4)
        self.assertTrue(cart)

    def test_hot_deal_view_post_anonymous_user(self):
        """
        Test that when an anonymous user makes a post on the hot deal
        view page
            - That the user is redirected to the before_checkout_anonymous
            page
        """
        self.cosmas = Client()
        response = self.cosmas.post(
            "/hot_deal/{}/".format(self.hot_deal.pk),
            {'phone_model_item': self.samsung_note_5_rose_gold.pk,
             'quantity': 2, 'owner': ''})
        self.assertRedirects(response, "/before_checkout_anonymous")
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2
        )
        self.assertTrue(cart)
