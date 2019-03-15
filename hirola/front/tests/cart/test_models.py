"""Test the models of a cart"""
from front.base_test import BaseTestCase
from front.models import User


class CartModelsTestCase(BaseTestCase):
    """Tests the cart models"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(CartModelsTestCase, self).setUp()
        User.objects.create_user(email="aladdin@gmail.com")
        self.aladdin = User.objects.get(email="aladdin@gmail.com")

    def test_cart_successful_creation(self):
        """
        Test that when you provide data to the admin page to create a cart,
        and the data provided is accurate:
            - That a cart is created successfully
        """
        data = {"owner": self.aladdin.pk, "quantity": 1,
                "phone_model_item": self.samsung_note_5_rose_gold.pk}
        post_response = self.elena.post("/admin/front/cart/add/", data)
        self.assertRedirects(post_response, "/admin/front/cart/")

    def test_cart_requires_quantity(self):
        """
        Test that when adding a cart object without a quantity being provided
            - That the page does not redirect
            - That an error is raised
        """
        data = {"owner": self.aladdin.pk,
                "phone_model_item": self.samsung_note_5_rose_gold.pk}
        post_response = self.elena.post("/admin/front/cart/add/", data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "This field is required.")

    def test_cart_quantity_not_negative(self):
        """
        Test that the quantity object of a cart cannot be negative
        """
        data = {"owner": self.aladdin.pk, "quantity": -1,
                "phone_model_item": self.samsung_note_5_rose_gold.pk}
        post_response = self.elena.post("/admin/front/cart/add/", data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(
            post_response, "Ensure this value is greater than or equal to 1.")

    def test_phone_item_id_required(self):
        """
        Test that when creating a cart object without a phone_model_list
        object
            - That the page does not redirect
            - That an error is raised
        """
        data = {"owner": self.aladdin.pk, "quantity": 1}
        post_response = self.elena.post("/admin/front/cart/add/", data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(
            post_response, "This field is required.")

    def test_owner_of_cart_can_be_null(self):
        """
        Test that when creating a cart object without specifying an owner
            - That the cart object can be created without the owner.
        """
        data = {"quantity": 1,
                "phone_model_item": self.samsung_note_5_rose_gold.pk}
        post_response = self.elena.post("/admin/front/cart/add/", data)
        self.assertRedirects(post_response, "/admin/front/cart/")
