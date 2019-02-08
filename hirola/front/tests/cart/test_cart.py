"""Test shopping logic."""
from front.base_test import (PhoneList, PhonesColor, BaseTestCase,
                             CountryCode, User, OrderStatus)


class ConfirmBeforeCartTestCase(BaseTestCase):

    def setUp(self):
        super(ConfirmBeforeCartTestCase, self).setUp()
        user_data = ConfirmBeforeCartTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        html_content = "Please confirm your email address"
        self.assertContains(response, html_content)
        user = User.objects.get(email="urieltimanko@example.com")
        user.is_active = True
        user.save()
        PhoneList.objects.create(category=self.android, currency=self.currency_v,
                                 price=10000, phone_name="Samsung Galaxy Edge", size_sku=self.size_android)
        self.mulika = PhoneList.objects.get(phone_name="Samsung Galaxy Edge")
        PhonesColor.objects.create(phone=self.mulika, size=4,
                                   abbreviation='GB', price=10000,
                                   quantity=5, is_in_stock=True,
                                   color=self.color_one)
        OrderStatus.objects.create(status='pending')

    def test_cannot_shop_unless_logged_in(self):
        """Test user needs to login to shop."""
        get_response = self.client.get("/phone_category/{}/".format(self.android.pk))
        self.assertContains(get_response, 'Select your favorite Android')
        self.assertContains(get_response, "Samsung Galaxy Edge")
        self.assertContains(get_response, "10000")
        form = {'quantity': 3, 'cart_item_add': self.mulika.pk, 'price': 10000}
        get_response_2 = self.client.post("/profile/{}/".format(self.mulika.pk), form, follow=True)
        self.assertRedirects(get_response_2, "/login?next=/profile/{}/".format(self.mulika.pk), 302)

    def test_shop_if_logged_in(self):
        """Test user needs to login to shop."""
        user_data = {"email": "urieltimanko@example.com",
                     "password": "*&#@&!*($)lp"}
        response = self.client.post('/login', user_data)
        self.assertRedirects(response, "/", 302)
        get_response = self.client.get("/phone_category/{}/".format(self.android.pk))
        self.assertContains(get_response, "Samsung Galaxy Edge")
        form = {'quantity': 3, 'cart_item_add': self.mulika.pk, 'cart_phone_price': 10000}
        get_response_2 = self.client.post("/profile/{}/".format(self.mulika.pk), form, follow=True)
        self.assertRedirects(get_response_2, '/before_checkout', 302)
        self.assertContains(get_response_2, "Samsung Galaxy Edge")
        self.assertContains(get_response_2, "<h6>Total <span class=\"right\">30000</span></h6>")
        self.assertContains(get_response_2, '<p>Quantity (3)</p>')
        self.assertContains(get_response_2, '<p>item(s)<span class="right">1</span></p>')



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