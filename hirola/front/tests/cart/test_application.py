"""Test the views of a cart"""
from front.base_test import BaseTestCase
from front.models import Cart, User, CartOwner
from front.views import (remove_cart_item, save_cart_item, change_quantity,
                         add_cart, before_add_cart)
from django.test import Client


class CartViewsTestCase(BaseTestCase):
    """Tests the cart views"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(CartViewsTestCase, self).setUp()

    def test_remove_cart_item(self):
        """
        Test that when you pass a cart id for a Cart you want to remove
            - That it no longer exists
        """
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold, quantity=3)
        cart_1 = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold, quantity=3
        )
        self.assertTrue(cart_1)
        remove_cart_item(cart_1.id)
        cart_after_delete = Cart.objects.filter(
            phone_model_item=self.samsung_note_5_rose_gold, quantity=3
        ).first()
        self.assertFalse(cart_after_delete)

    def test_save_cart_item(self):
        """
        Test that when you pass a cart id for a Cart that you want to be in
        the Wishlist
            - That its wishlist value becomes True
        """
        Cart.objects.create(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4)
        cart_2 = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4
        )
        self.assertEqual(cart_2.is_wishlist, False)
        save_cart_item(cart_2.id)
        cart_2_wishlist = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4
        )
        self.assertEqual(cart_2_wishlist.is_wishlist, True)

    def test_change_quantity(self):
        """
        Test that when you pass the cart id and a quantity for a cart that you
        desire to change its quantity
            - That the quantity changes to the quantity you select
        """
        Cart.objects.create(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4)
        cart_2 = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold, quantity=4
        )
        self.assertEqual(cart_2.quantity, 4)
        change_quantity(cart_2.id, 2)
        cart_2_quantity = Cart.objects.get(
            phone_model_item=self.samsung_note_7_rose_gold
        )
        self.assertEqual(cart_2_quantity.quantity, 2)

    def test_add_cart(self):
        """
        Test that when a Cart for an anonymous user with a session_key is
        created then a request with the session_key, and a user is passed to
        the add_cart method:
            - That the cart owner is changed from None to the user passed to
            the method
            - That the session key is set to None.
            - That the CartOwner object is deleted.
        """
        self.winniethepooh = Client()
        Cart.objects.create(phone_model_item=self.samsung_note_5_rose_gold,
                            quantity=3,
                            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            session_key=self.winniethepooh.session.session_key)
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        before_add_cart(self.winniethepooh, user)
        self.assertEqual(cart.owner, None)
        self.assertEqual(
            cart.session_key, self.winniethepooh.session.session_key)
        cart_owner = CartOwner.objects.filter(owner=user, cart=cart).first()
        self.assertTrue(cart_owner)
        add_cart(self.winniethepooh, user)
        after_cart = Cart.objects.get(id=cart.id)
        self.assertEqual(after_cart.owner, user)
        self.assertEqual(after_cart.session_key, None)
        cart_owner = CartOwner.objects.filter(owner=user, cart=cart).first()
        self.assertFalse(cart_owner)

    def test_before_add_cart(self):
        """
        Test that the before_add_cart method creates a cart_owner object
        """
        self.winniethepooh = Client()
        Cart.objects.create(phone_model_item=self.samsung_note_5_rose_gold,
                            quantity=3,
                            session_key=self.winniethepooh.session.session_key)
        cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold,
            session_key=self.winniethepooh.session.session_key)
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        before_add_cart(self.winniethepooh, user)
        cart_owner = CartOwner.objects.filter(owner=user, cart=cart).first()
        self.assertTrue(cart_owner)
        self.assertEqual(cart_owner.owner, user)
        self.assertEqual(cart_owner.cart, cart)
