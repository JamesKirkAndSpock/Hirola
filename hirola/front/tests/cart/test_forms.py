"""Test the forms for a cart"""
from front.base_test import BaseTestCase
from front.forms.cart_forms import CartForm
from django.test import RequestFactory, Client
from django.contrib import auth
from django.contrib.sessions.middleware import SessionMiddleware
from front.models import User, Cart
from front.views import check_cart_exists
from front.views import check_cart_exists_anonymous


class CartFormTestCase(BaseTestCase):
    """Tests the CartForm form methods and functionality"""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(CartFormTestCase, self).setUp()

    def test_successful_validation(self):
        """
        Test that when a form is provided with valid data
            - That the form validation is True
        """
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk,
                 'quantity': 1, 'owner': '',
                 'session_key': ''}
            )
        self.client = Client()
        self.client.get("/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = auth.get_user(self.client)
        form = CartForm(request, request.POST)
        self.assertTrue(form.is_valid())

    def test_anonymous_user_cart_form(self):
        """
        Test that if a user provided to the CartForm is not anonymous:
            - That a cart is created for the specific user on save
        """
        User.objects.create_user(email="example_user@gmail.com")
        user = User.objects.get(email="example_user@gmail.com")
        self.client = Client()
        self.client.get("/")
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk,
                 'quantity': 1, 'owner': user.pk,
                 'session_key': ''}
            )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = auth.get_user(self.client)
        form = CartForm(request, request.POST)
        self.assertTrue(form.is_valid())
        form.save()
        cart = Cart.objects.get(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1)
        self.assertTrue(cart)

    def test_quantity_user_cart_form(self):
        """
        Test that if a quantity is provided to the CartForm for an existent
        cart:
            - That the quantity is added to what was there before
        """
        User.objects.create_user(email="example_user@gmail.com")
        user = User.objects.get(email="example_user@gmail.com")
        self.client = Client()
        self.client.get("/")
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk,
                 'quantity': 7, 'owner': user.pk,
                 'session_key': ''}
            )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = auth.get_user(self.client)
        Cart.objects.create(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1)
        cart = Cart.objects.get(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1
        )
        form = CartForm(request, request.POST, instance=cart)
        self.assertTrue(form.is_valid())
        form.save()
        edited_cart = Cart.objects.get(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold)
        self.assertEqual(edited_cart.quantity, 8)

    def test_session_key_cart_form(self):
        """
        Test that if an anonymous user is provided to the CartForm:
            - That the session key is added
        """
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk,
                 'quantity': 1, 'owner': '',
                 'session_key': ''}
            )
        self.client = Client()
        self.client.get("/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = auth.get_user(self.client)
        form = CartForm(request, request.POST)
        self.assertTrue(form.is_valid())
        form.save()
        added_cart = Cart.objects.get(
            phone_model_item=self.samsung_note_5_rose_gold)
        self.assertTrue(added_cart.session_key)
        self.assertFalse(added_cart.owner)

    def test_cart_form_returned_existing_cart(self):
        """
        Test that the cart form for a request for a user returns a form
        instance that is to be edited.
        """
        User.objects.create_user(email="example_user@gmail.com")
        user = User.objects.get(email="example_user@gmail.com")
        Cart.objects.create(
            owner=user, phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1)
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk}
            )
        self.client = Client()
        request.user = user
        form = check_cart_exists(request)
        self.assertEqual(form.instance.owner, user)
        self.assertEqual(
            form.instance.phone_model_item, self.samsung_note_5_rose_gold)
        self.assertEqual(
            form.instance.quantity, 1)

    def test_cart_form_no_cart(self):
        """
        Test that the cart form for a request for a user returns an instance
        that has None values
        """
        User.objects.create_user(email="example_user@gmail.com")
        user = User.objects.get(email="example_user@gmail.com")
        request = RequestFactory()
        request = request.post(
            "", {}
            )
        self.client = Client()
        request.user = user
        form = check_cart_exists(request)
        self.assertEqual(form.instance.owner, None)
        self.assertEqual(form.instance.session_key, None)

    def test_cart_form_returned_existing_cart_anonymous(self):
        """
        Test that the cart form for a request for a user returns a form
        instance that is to be edited.
        """
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1)
        request = RequestFactory()
        request = request.post(
            "", {'phone_model_item': self.samsung_note_5_rose_gold.pk}
            )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        self.client = Client()
        request.user = auth.get_user(self.client)
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=1, session_key=request.session.session_key)
        form = check_cart_exists_anonymous(request)
        self.assertEqual(form.instance.owner, None)
        self.assertEqual(
            form.instance.phone_model_item, self.samsung_note_5_rose_gold)
        self.assertEqual(
            form.instance.quantity, 1)

    def test_cart_form_no_cart_anonymous(self):
        """
        Test that the cart form for a request for a user returns an instance
        that has None values
        """
        request = RequestFactory()
        request = request.post(
            "", {}
            )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        self.client = Client()
        request.user = auth.get_user(self.client)
        form = check_cart_exists_anonymous(request)
        self.assertEqual(form.instance.owner, None)
        self.assertEqual(form.instance.session_key, None)
