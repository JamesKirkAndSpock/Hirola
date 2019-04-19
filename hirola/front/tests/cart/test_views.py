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
        msg_1 = ("Looks like you haven't added any items to your cart! "
                 "Visit our")
        msg_2 = "and find the phone you desire"
        msg_3 = "tunafurahia sana kukuwezesha kupata teknologia halali"
        self.assertContains(response, msg_1)
        self.assertContains(response, msg_2)
        self.assertContains(response, msg_3)

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
                            quantity=3, owner=user)
        cart = Cart.objects.get(phone_model_item=self.samsung_note_5_rose_gold,
                                owner=user)
        Cart.objects.create(phone_model_item=self.samsung_note_7_rose_gold,
                            quantity=2, owner=user)
        self.winniethepooh.force_login(user)
        Feature.objects.create(
            phone=self.samsung_note_5_rose_gold, feature="GSM feature")
        response = self.winniethepooh.get("/before_checkout")
        msg = "Howdy folk!, looks like you havent added anything to the cart!"
        note_7_quantity = "<option value=\"2\" selected>2</option>"
        note_5_quantity = "<option value=\"3\" selected>3</option>"
        self.assertNotContains(response, msg)
        self.assertContains(response, cart.phone_model_item)
        self.assertContains(response, cart.phone_model_item.size_sku)
        self.assertContains(response, cart.phone_model_item.main_image)
        self.assertContains(response, note_7_quantity)
        self.assertContains(response, note_5_quantity)
        self.assertContains(response, "GSM feature")
        self.assertContains(response, "75,000")
        self.assertContains(response, "<span class=\"right\">2</span>")
        self.assertContains(response, "125,000")

    def test_before_checkout_anonymous_no_cart(self):
        """
        Test that when a user has no cart and the user visits the before
        checkout anonymous view:
            - That the page displays the Howdy folk message
        """
        self.winniethepooh = Client()
        response = self.winniethepooh.get("/before_checkout_anonymous")
        msg_1 = ("Looks like you haven't added any items to your cart! "
                 "Visit our")
        msg_2 = "and find the phone you desire"
        msg_3 = "tunafurahia sana kukuwezesha kupata teknologia halali"
        self.assertContains(response, msg_1)
        self.assertContains(response, msg_2)
        self.assertContains(response, msg_3)

    def test_before_checkout_anonymous_data_rendered(self):
        """
        Test that when a user has a cart and the user visits the before
        checkout anonymous view:
            - That the page displays the data.
        """
        self.winniethepooh = Client()
        response = self.winniethepooh.get("/before_checkout_anonymous")
        Cart.objects.create(phone_model_item=self.samsung_note_5_rose_gold,
                            quantity=3,
                            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            session_key=self.winniethepooh.session.session_key)
        Cart.objects.create(phone_model_item=self.samsung_note_7_rose_gold,
                            quantity=2,
                            session_key=self.winniethepooh.session.session_key)
        note_7_quantity = "<option value=\"2\" selected>2</option>"
        note_5_quantity = "<option value=\"3\" selected>3</option>"
        Feature.objects.create(
            phone=self.samsung_note_5_rose_gold, feature="GSM feature")
        response = self.winniethepooh.get("/before_checkout_anonymous")
        self.assertContains(response, note_7_quantity)
        self.assertContains(response, note_5_quantity)
        self.assertContains(response, cart.phone_model_item)
        self.assertContains(response, cart.phone_model_item.size_sku)
        self.assertContains(response, cart.phone_model_item.main_image)
        self.assertContains(response, "GSM feature")
        self.assertContains(response, "75,000")
        self.assertContains(response, "<span class=\"right\">2</span>")
        self.assertContains(response, "125,000")

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

    def test_remove_cart_before_checkout_anonymous(self):
        """
        Test that if a Post request is made on the before_checkout_anonymous
        page with the cart id to remove
            - That the cart will be removed.
        """
        self.winniethepooh = Client()
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10,
            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10,
            session_key=self.winniethepooh.session.session_key)
        response = self.winniethepooh.get("/before_checkout_anonymous")
        self.assertContains(response, "Samsung Note 5")
        data = {"cart_id_remove": cart.id}
        after_remove_response = self.winniethepooh.post(
            "/before_checkout_anonymous", data)
        self.assertNotContains(after_remove_response, "Samsung Note 5")

    def test_save_cart_before_checkout_anonymous(self):
        """
        Test that if a Post request is made on the before_checkout_anonymous
        page with the cart id to save
            - That the wishlist appears for the user
        """
        self.winniethepooh = Client()
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10,
            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10,
            session_key=self.winniethepooh.session.session_key)
        response = self.winniethepooh.get("/before_checkout_anonymous")
        self.assertContains(response, "Samsung Note 5")
        data = {"cart_id_save": cart.id}
        after_save_response = self.winniethepooh.post(
            "/before_checkout_anonymous", data)
        self.assertEqual(after_save_response.status_code, 200)

    def test_remove_cart_before_checkout(self):
        """
        Test that if a Post request is made on the before_checkout
        page with the cart id to remove
            - That the cart will be removed.
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10, owner=user)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10, owner=user)
        response = self.winniethepooh.get("/before_checkout")
        self.assertContains(response, "Samsung Note 5")
        data = {"cart_id_remove": cart.id}
        after_remove_response = self.winniethepooh.post(
            "/before_checkout", data)
        self.assertNotContains(after_remove_response, "Samsung Note 5")

    def test_save_cart_before_checkout(self):
        """
        Test that if a Post request is made on the before_checkout
        page with the cart id to save
            - That the wishlist appears for the user
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10, owner=user)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=10, owner=user)
        response = self.winniethepooh.get("/before_checkout")
        self.assertContains(response, "Samsung Note 5")
        data = {"cart_id_save": cart.id}
        after_save_response = self.winniethepooh.post(
            "/before_checkout", data)
        self.assertEqual(after_save_response.status_code, 200)

    def test_change_quantity_before_checkout(self):
        """
        Test that if a Post request is made on the before_checkout
        page with quantity to change
            - That the price and total price change
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_7_rose_gold,
            quantity=1, owner=user)
        cart_2 = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold,
            quantity=1, owner=user)
        response = self.winniethepooh.get("/before_checkout")
        self.assertContains(response, "Samsung Note 5")
        self.assertContains(response, "50,000")
        self.assertContains(response, "75,000")
        cart_2_data = {"quantity": 2, "cart_id_quantity": cart_2.id}
        self.winniethepooh.post("/before_checkout", cart_2_data)
        data = {"quantity": 3, "cart_id_quantity": cart.id}
        after_save_response = self.winniethepooh.post(
            "/before_checkout", data)
        self.assertEqual(after_save_response.status_code, 200)
        self.assertContains(after_save_response, "75,000")
        self.assertContains(after_save_response, "125,000")

    def test_buy_now_anonymous(self):
        """
        Test that when a user request to buy now before logging in
            - That their item is saved to the cart
            - and they are prompted to login in before proceeding
        """
        form = {
            'buy_now': '1',
            'quantity': '1',
            'phone_model_input': '{}'.format(
                self.samsung_note_5_rose_gold.phone_model.id),
            'phone_model_item': '{}'.format(
                self.samsung_note_5_rose_gold.id)
        }
        response = self.client.post('/profile/{}/'.format(
            self.samsung_note_5_rose_gold.pk), form, follow=True)
        self.assertRedirects(response, "/login?next=/checkout")
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold)
        self.assertTrue(cart)
