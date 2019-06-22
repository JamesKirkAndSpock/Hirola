from front.base_test import BaseTestCase, User, Cart
from front.models import ShippingAddress
from front.forms.cart_forms import send_order_notice_email
from django.test import RequestFactory
from django.core import mail
from front.views import get_cart_total
from django.conf import settings
from django.template.loader import render_to_string


class NoticeEmailTestCase(BaseTestCase):
    """
    Test sending email after user places order.
    """

    def setUp(self):
        """Setup email tests preconditions."""
        super(NoticeEmailTestCase, self).setUp()

    def test_order_notice_email_sent(self):
        """
        Test user
        """
        request = RequestFactory()
        request = request.post(
            "", {'email': 'naisomia@gmail.com', 'password': 'secret'}
            )
        User.objects.create_user(email="sivanna@gmail.com", password="secret")
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=2, owner=user)
        cart = Cart.objects.filter(owner=request.user)
        shipping_address = ShippingAddress.objects.create(
            pickup=False,
            location='Kibera',
            phone_number=712893454
        )
        send_order_notice_email(
            request, user, cart, get_cart_total(cart), shipping_address)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['sivanna@gmail.com'])
        subject = "Order Confirmation"
        self.assertEqual(mail.outbox[0].subject, subject)
        body_content = "Thanks for shopping at teke"
        rendered = str(mail.outbox[0].body)
        self.assertIn(body_content, rendered)
        item_detail = "<li style=\"list-style: decimal\">".format(
            "<span class=\"text-title\" style=\"font-weight: 600\">"
            "Samsung Note 5</span> Ksh. 25000</li>")
        self.assertIn(item_detail, rendered)
        shipping = "<span class=\"text-title\" style=\"font-weight: 600\">"\
                   "Town:</span> Kibera"
        self.assertIn(shipping, rendered)
        item_title = "<span class=\"text-title\" id=\"total\" "\
                     "style=\"font-weight: 600; margin-left: 20px\">"\
                     "Order Total: Ksh. </span>50000"
        self.assertIn(item_title, rendered)
