"""Test the views of a cart"""
from front.base_test import BaseTestCase
from front.models import Cart
from front.views import remove_cart_item, save_cart_item


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
