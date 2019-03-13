"""Test the views of a cart"""
from front.base_test import BaseTestCase
from front.models import Cart, User, Feature
from front.views import get_cart_total
from django.test import Client


class CartViewsTestCase(BaseTestCase):
    """Tests the cart views"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(CartViewsTestCase, self).setUp()

    def test_get_cart_total(self):
        """
        Test that when you provide Cart items to the get_cart_total method
            - That you get accurate results as per the cart totals
        """
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold, quantity=3)
        Cart.objects.create(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4)
        Cart.objects.create(
            phone_model_item=self.iphone_6_s_rose_gold, quantity=5)
        cart_1 = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold, quantity=3
        )
        cart_2 = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4
        )
        cart_3 = Cart.objects.get(
            phone_model_item=self.iphone_6_s_rose_gold, quantity=5
        )
        items_list = [cart_1, cart_2, cart_3]
        total = get_cart_total(items_list)
        self.assertEqual(total, 300000)

    def test_before_checkout_view(self):
        """
        Test that when you visit the before_checkout URL:
            - That the user has to be logged in
        """
        response = self.client.get("/before_checkout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/before_checkout")

    def test_before_checkout_view_logged_in_user(self):
        """
        Test that when a logged in user visits the before_checkout view:
            - That if he has no cart items he gets a welcome message
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        response = self.winniethepooh.get("/before_checkout")
        msg = "Howdy folk!, looks like you havent added anything to the cart!"
        self.assertContains(response, msg)

    def test_before_checkout_view_data_rendered(self):
        """
        Test that when a logged in user visits the before_checkout view and
        the user owns some Carts:
            - That the data for the carts is rendered
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        Cart.objects.create(phone_model_item=self.samsung_note_5_rose_gold,
                            quantity=10, owner=user)
        cart = Cart.objects.get(phone_model_item=self.samsung_note_5_rose_gold,
                                owner=user)
        Cart.objects.create(phone_model_item=self.samsung_note_7_rose_gold,
                            quantity=2, owner=user)
        self.winniethepooh.force_login(user)
        Feature.objects.create(
            phone=self.samsung_note_5_rose_gold, feature="GSM feature")
        response = self.winniethepooh.get("/before_checkout")
        msg = "Howdy folk!, looks like you havent added anything to the cart!"
        self.assertNotContains(response, msg)
        self.assertContains(response, cart.phone_model_item)
        self.assertContains(response, cart.phone_model_item.size_sku)
        self.assertContains(response, "Quantity ({})".format(cart.quantity))
        self.assertContains(response, cart.phone_model_item.main_image)
        self.assertContains(response, "GSM feature")
        self.assertContains(response, "250,000")
        self.assertContains(response, "<span class=\"right\">2</span>")
        self.assertContains(response, "300,000")

    def test_before_checkout_anonymous_no_cart(self):
        """
        Test that when a user has no cart and the user visits the before
        checkout anonymous view:
            - That the page displays the Howdy folk message
        """
        self.winniethepooh = Client()
        response = self.winniethepooh.get("/before_checkout_anonymous")
        msg = "Howdy folk!, looks like you havent added anything to the cart!"
        self.assertContains(response, msg)

    def test_before_checkout_anonymous_data_rendered(self):
        """
        Test that when a user has a cart and the user visits the before
        checkout anonymous view:
            - That the page displays the data.
        """
        self.winniethepooh = Client()
        response = self.winniethepooh.get("/before_checkout_anonymous")
        Cart.objects.create(phone_model_item=self.samsung_note_5_rose_gold,
                            quantity=10,
                            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            session_key=self.winniethepooh.session.session_key)
        Cart.objects.create(phone_model_item=self.samsung_note_7_rose_gold,
                            quantity=2,
                            session_key=self.winniethepooh.session.session_key)
        Feature.objects.create(
            phone=self.samsung_note_5_rose_gold, feature="GSM feature")
        response = self.winniethepooh.get("/before_checkout_anonymous")
        self.assertContains(response, cart.phone_model_item)
        self.assertContains(response, cart.phone_model_item.size_sku)
        self.assertContains(response, "Quantity ({})".format(cart.quantity))
        self.assertContains(response, cart.phone_model_item.main_image)
        self.assertContains(response, "GSM feature")
        self.assertContains(response, "250,000")
        self.assertContains(response, "<span class=\"right\">2</span>")
        self.assertContains(response, "300,000")

    def test_phone_profile_view_post_logged_in(self):
        """
        Test that when an identified user makes a post on the phone profile
        view page
            - That the user is redirected to the before_checkout page
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        response = self.winniethepooh.post(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.pk),
            {'phone_model_item': self.samsung_note_5_rose_gold.pk,
             'quantity': 2, 'owner': '', 'session_key': ''})
        self.assertRedirects(response, "/before_checkout")
        cart = Cart.objects.get(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2)
        self.assertTrue(cart)

    def test_phone_profile_view_post_anonymous_user(self):
        """
        Test that when an anonymous user makes a post on the phone profile
        view page
            - That the user is redirected to the before_checkout_anonymous
            page
        """
        self.cosmas = Client()
        response = self.cosmas.post(
            "/profile/{}/".format(self.samsung_note_5_rose_gold.pk),
            {'phone_model_item': self.samsung_note_5_rose_gold.pk,
             'quantity': 2, 'owner': ''})
        self.assertRedirects(response, "/before_checkout_anonymous")
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2
        )
        self.assertTrue(cart)
