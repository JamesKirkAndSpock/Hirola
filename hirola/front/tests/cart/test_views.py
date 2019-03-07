"""Test shopping logic."""
from front.base_test import (PhoneList, PhonesColor, BaseTestCase, User)
from front.views import get_cart_total, get_cart_object
from front.models import (CountryCode, OrderStatus, Order, Cart, SocialMedia)


class ConfirmBeforeCartTestCase(BaseTestCase):
    """Tests the cart."""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        super(ConfirmBeforeCartTestCase, self).setUp()
        user_data = ConfirmBeforeCartTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        html_content = "Please confirm your email address"
        self.assertContains(response, html_content)
        self.user = User.objects.get(email="urieltimanko@example.com")
        self.user.is_active = True
        self.user.save()
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=10000,
                                 phone_name="Samsung Galaxy Edge",
                                 size_sku=self.size_android)
        self.mulika = PhoneList.objects.get(phone_name="Samsung Galaxy Edge")
        Cart.objects.create(owner=self.user)
        self.cart = Cart.objects.get(owner=self.user.pk)
        PhonesColor.objects.create(
            phone=self.mulika, size=self.size_android, price=10000,
            quantity=5, is_in_stock=True, color=self.color_one)
        OrderStatus.objects.create(status='pending')
        self.status = OrderStatus.objects.get(status="pending")

    def test_get_cart_total(self):
        """Test functionality to calculate cart total."""
        Order.objects.create(
            owner=self.user, phone=self.samsung_note_5_rose_gold,
            status=self.status, quantity=2, price=25000,
            total_price=50000, cart=self.cart
            )
        Order.objects.create(
            owner=self.user, phone=self.samsung_note_5_rose_gold,
            status=self.status, quantity=2, price=25000,
            total_price=25000, cart=self.cart
            )
        order = Order.objects.filter(owner=self.user)
        total = get_cart_total(order)
        self.assertEqual(total, 75000)

    def test_get_cart_object(self):
        """
        Test that when a client without a session cart_id is passed to the
        get_cart_object method
            -  That an istances of the cart object is returned
        """
        cart_object = get_cart_object(self.client)
        self.assertIsInstance(cart_object, Cart)

    def test_get_cart_object_with_session(self):
        """
        Test that when a client wit a session cart_id is passed to the
        get_cart_object method
            - That the cart with the owner's name is returned
        """
        Cart.objects.create(id=12345, owner=self.user)
        client_session = self.client.session
        client_session.update({"cart_id": 12345})
        client_session.save()
        cart_object = get_cart_object(self.client)
        self.assertIsInstance(cart_object, Cart)
        self.assertIn("Uriel Timanko", str(cart_object))

    def generate_user_data(self, data):
        '''
        Generate data for a user to be posted to the signup page
        '''
        country_code = CountryCode.objects.filter(country_code=254).first()
        user_data = {"first_name": data.get('first_name') or "Uriel",
                     "last_name": data.get('last_name') or "Timanko",
                     "country_code": country_code.id,
                     "phone_number": data.get('phone_number') or 722000000,
                     "email": data.get('email') or "urieltimanko@example.com",
                     "password1": data.get('password1') or "*&#@&!*($)lp",
                     "password2": data.get('password2') or "*&#@&!*($)lp"}
        return user_data

    def test_categories_social_media_cart_page(self):
        """
        Test that when you visit the /before_checkout page
            - That the phone categories and social media are rendered
        """
        SocialMedia.objects.create(
            url_link="https://instagram.com", icon="fa fa-instagram",
            name="Instagram")
        get_response = self.client.get("/before_checkout")
        self.assertContains(get_response, self.iphone)
        self.assertContains(get_response, self.android)
        self.assertContains(get_response, self.tablet)
        self.assertContains(get_response, "Instagram")

    def test_cart_as_string(self):
        """
        Test the string representation of a cart
            - That the cart renders the string Anonymous User in case no user
            owns it
            - That the cart renders the email of the User in case a user owns
            it
        """
        self.assertIn("Uriel Timanko", str(self.cart))
        Cart.objects.create(owner=None)
        cart_object = Cart.objects.get(owner=None)
        self.assertIn("Uriel Timanko", str(self.cart))
        self.assertIn("Anonymouse User", str(cart_object))
