"""Test shopping logic."""
from front.base_test import (PhoneList, PhonesColor, BaseTestCase,
                             CountryCode, User, OrderStatus, Order)
from front.views import get_cart_total


class ConfirmBeforeCartTestCase(BaseTestCase):

    def setUp(self):
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
        PhonesColor.objects.create(phone=self.mulika, size=4,
                                   abbreviation='GB', price=10000,
                                   quantity=5, is_in_stock=True,
                                   color=self.color_one)
        OrderStatus.objects.create(status='pending')

    def test_get_cart_total(self):
        """Test functionality to calculate cart total."""
        status = OrderStatus.objects.get(status="pending")
        Order.objects.create(
            owner=self.user, phone=self.mulika, status=status, quantity=2,
            price=25000, total_price=50000)
        Order.objects.create(
            owner=self.user, phone=self.mulika, status=status, quantity=2,
            price=25000, total_price=25000)
        order = Order.objects.filter(owner=self.user)
        total = get_cart_total(order)
        self.assertEqual(total, 75000)

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