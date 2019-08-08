"""Test the views of checkout page"""
from front.base_test import BaseTestCase
from front.models import Cart, User, Feature, Order, PhoneModelList
from django.test import Client


class CheckoutViewTestCase(BaseTestCase):
    """Tests the cart views"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(CheckoutViewTestCase, self).setUp()

    def test_checkout_cart_items(self):
        """
        Test that when you visit the /checkout page that you can view images
        and data for phones rendered
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
        response = self.winniethepooh.get("/checkout")
        note_7_quantity = "<option value=\"2\" selected>2</option>"
        note_5_quantity = "<option value=\"3\" selected>3</option>"
        self.assertContains(response, cart.phone_model_item)
        self.assertContains(response, cart.phone_model_item.size_sku)
        self.assertContains(response, cart.phone_model_item.main_image)
        self.assertContains(response, note_7_quantity)
        self.assertContains(response, note_5_quantity)
        self.assertContains(response, "GSM feature")
        self.assertContains(response, "75,000")
        self.assertContains(response, "125,000")

    def test_before_checkout_with_no_cart(self):
        """
        Test that when a user has no cart and the user visits the
        checkout page:
            - That the page displays the a message for not adding a cart
            - That the page redirects to the before_cheeckout page
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        response = self.winniethepooh.get("/checkout", follow=True)
        self.assertRedirects(response, "/before_checkout")
        msg_1 = ("Looks like you haven't added any items to your cart! "
                 "Visit our")
        msg_2 = "and find the phone you desire"
        msg_3 = "tunafurahia sana kukuwezesha kupata teknologia halali"
        self.assertContains(response, msg_1)
        self.assertContains(response, msg_2)
        self.assertContains(response, msg_3)

    def test_remove_cart_checkout(self):
        """
        Test that if a Post request is made on the checkout
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
        response = self.winniethepooh.get("/checkout")
        self.assertContains(response, "Samsung Note 5")
        data = {"cart_id_remove": cart.id}
        after_remove_response = self.winniethepooh.post(
            "/before_checkout", data)
        self.assertNotContains(after_remove_response, "Samsung Note 5")

    def test_change_quantity_checkout(self):
        """
        Test that if a Post request is made on the checkout
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
        response = self.winniethepooh.get("/checkout")
        self.assertContains(response, "Samsung Note 5")
        self.assertContains(response, "50,000")
        self.assertContains(response, "75,000")
        cart_2_data = {"quantity": 2, "cart_id_quantity": cart_2.id}
        self.winniethepooh.post("/checkout", cart_2_data)
        data = {"quantity": 3, "cart_id_quantity": cart.id}
        after_save_response = self.winniethepooh.post(
            "/before_checkout", data)
        self.assertEqual(after_save_response.status_code, 200)
        self.assertContains(after_save_response, "75,000")
        self.assertContains(after_save_response, "125,000")

    def test_order_items(self):
        """
        Test that when a client clicks the place order button
            - That the items in the cart are converted to orders
            - That their cart is emptied
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        Cart.objects.create(
            phone_model_item=self.samsung_note_7_rose_gold,
            quantity=1, owner=user)
        response = self.winniethepooh.post('/order')
        self.assertRedirects(response, '/dashboard#orders', 302)
        order_1 = Order.objects.get(phone=self.samsung_note_5_rose_gold)
        self.assertEqual(order_1.owner, user)
        orders = Order.objects.all()
        self.assertEqual(len(orders), 2)
        carts = Cart.objects.filter(owner=user)
        self.assertEqual(len(carts), 0)

    def test_item_quantity_reduced(self):
        """
        Test that when a client order's an item
            - That its quantity is reduced by the number
              of items ordered
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        phone = PhoneModelList.objects.get(
            id=self.samsung_note_5_rose_gold.pk)
        self.assertEqual(phone.quantity, 4)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        response = self.winniethepooh.post('/order')
        self.assertRedirects(response, '/dashboard#orders', 302)
        phone = PhoneModelList.objects.get(
            id=self.samsung_note_5_rose_gold.pk)
        self.assertEqual(phone.quantity, 2)
        # if item's quantity gets to zero, the item should not be in stock
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        response = self.winniethepooh.post('/order')
        self.assertRedirects(response, '/dashboard#orders', 302)
        phone = PhoneModelList.objects.get(
            id=self.samsung_note_5_rose_gold.pk)
        self.assertEqual(phone.quantity, 0)
        self.assertFalse(phone.is_in_stock)

    def test_get_order_url(self):
        """
        Test that when the order url is visited without posting any data
        - it redirects to the checkout page
        """
        self.winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        self.winniethepooh.force_login(user)
        response = self.winniethepooh.get('/order', follow=True)
        self.assertRedirects(response, '/before_checkout', 302)
