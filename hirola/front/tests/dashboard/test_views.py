"""Contains tests for dashboard views."""
from front.base_test import (BaseTestCase, Client)
from front.tests.test_users import UserSignupTestCase
from front.models import (
    Review, User, ShippingAddress, Order, OrderStatus, Cart, CancelledOrder)


class DashboardTemplate(BaseTestCase):

    def setUp(self):
        super(DashboardTemplate, self).setUp()
        user_data = UserSignupTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        html_content = "Please confirm your email address"
        self.assertContains(response, html_content)
        self.uriel = Client()
        user = User.objects.get(email="urieltimanko@example.com")
        user.is_active = True
        user.save()
        self.uriel.force_login(user)

    def test_user_data_on_dashboard(self):
        '''
        Test that when a logged in user accesses the /dashboard page that:
            - The page contains all the Phone Categories of the site
            - The page contains Social media links
            - The user is able to see his or her Firstname, LastName, Phone
            number, Country Code, Country
        '''
        response = self.uriel.get('/dashboard')
        self.assertContains(response, "Iphone")
        self.assertContains(response, "Android")
        self.assertContains(response, "Tablet")
        self.assertContains(response, "Uriel")
        self.assertContains(response, "Timanko")
        self.assertContains(response, 722000000)
        self.assertContains(response, 254)
        self.assertContains(response, "Kenya")

    def test_review_data_on_dashboard(self):
        '''
        Test that when a logged in user accesses the dashboard that:
            - The user is able to view his or her reviews on an item he or she
            bought.
        '''
        (owner, order) = self.generate_review_data()
        data = {"stars": 5, "comments": "Great job guys", "owner": owner.id,
                "phone_model": self.samsung_note_5.id}
        response = self.elena.post('/admin/front/review/add/', data)
        self.assertEqual(response.status_code, 302)
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, "Great job guys",)

    def test_stars_counter(self):
        '''
        Test that when a user visits the dashboard view to view ratings:
            - That the stars are rendered properly in terms of checked and
            unchecked stars
        '''
        (owner, order) = self.generate_review_data()
        data = []
        for i in range(5):
            data.append(
                {
                    "stars": i+1, "comments": "Great job guys",
                    "owner": owner.id, "phone_model": self.iphone_6_s.id
                    })
        checked_star = (
            "<i class=\"material-icons left checked\">grade</i>\n             "
            "               \n                            "
        )
        unchecked_star = (
            "<i class=\"material-icons left\">grade</i>\n      "
            "                      \n                            "
        )
        for i in range(5):
            self.elena.post('/admin/front/review/add/', data[i])
            response = self.uriel.get('/dashboard')
            self.assertContains(response, checked_star*(i+1))
            self.assertContains(response, unchecked_star*(4-i))
            Review.objects.get(stars=i+1).delete()

    def test_order_data_get_request(self):
        '''
        Test that if a moves to the dashboard, and that he had made
        some orders
            - That the order details for his past orders are rendered:
        '''
        (owner, order) = self.generate_review_data()
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, order.phone.phone_model)
        self.assertContains(
            get_response, "<p><b>Order No:</b><span> #{}</span>".
            format(order.pk))
        self.assertContains(
            get_response, "<b>Payment Method:</b><span> {}</span>".
            format(order.payment_method))
        self.assertContains(
            get_response, "<b>Quantity:</b><span> {}</span>".
            format(order.quantity))
        self.assertContains(
            get_response, "<b>Total Price:</b><span> {}</span>".
            format("{:,}".format(order.total_price)))
        self.assertContains(
            get_response, "<span> {}</span>".
            format(order.status))
        purchase_date = "<b>Purchase Date: </b><span id=\"purchaseDate\">"\
            "{}</span>".format(order.date.strftime("%b %d %Y %H:%M"))
        self.assertContains(
            get_response, purchase_date)
        self.assertContains(
            get_response, "<li>Recipient: {}</li>".
            format(owner))
        self.assertContains(
            get_response, "Location: {}".
            format(order.shipping_address.location))
        self.assertContains(
            get_response, "<li>Pick up: {}</li>".
            format(order.shipping_address.location))

    def test_order_data_post_request(self):
        '''
        Test that if a user moves to the dashboard, and that he had made
            some orders and he posts something:
            - That the order details for his past orders are rendered:
        '''
        winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        cart = Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=3, owner=user)
        data = {
            'hidden_pickup': 1,
            'country_code': self.code.id,
            'phone_number': '0715557775',
            'location': 'Rongai, Posta'}
        winniethepooh.force_login(user)
        post_response = winniethepooh.post('/order', data, follow=True)
        order = Order.objects.get(owner=user)
        self.assertContains(post_response, cart.phone_model_item)
        self.assertContains(
            post_response, "<p><b>Order No:</b><span> #{}</span>".
            format(order.pk))
        self.assertContains(
            post_response, "<b>Payment Method:</b><span> {}</span>".
            format(order.payment_method))
        self.assertContains(
            post_response, "<b>Quantity:</b><span> {}</span>".
            format(order.quantity))
        self.assertContains(
            post_response, "<b>Total Price:</b><span> {}</span>".
            format("{:,}".format(order.total_price)))
        self.assertContains(
            post_response, "<span> {}</span>".
            format(order.status))
        purchase_date = "<b>Purchase Date: </b><span id=\"purchaseDate\">"\
            "{}</span>".format(order.date.strftime("%b %d %Y %H:%M"))
        self.assertContains(
            post_response, purchase_date)
        self.assertContains(
            post_response, "<li>Recipient: {}</li>".
            format(user))
        self.assertContains(
            post_response, "Location: {}".format(
                order.shipping_address.location))
        self.assertContains(
            post_response, "Pick up: {}".
            format(order.shipping_address.location))
        self.assertContains(
            post_response, "<li>Phone No: {}</li>".
            format(order.shipping_address.phone_number))

    def test_order_to_pickup(self):
        """
        Test that a user can order to pickup from company premises
        """
        winniethepooh = Client()
        User.objects.create(email="winnie@thepooh.com")
        user = User.objects.get(email="winnie@thepooh.com")
        cart = Cart.objects.create(
            phone_model_item=self.samsung_note_5_rose_gold,
            quantity=3, owner=user)
        data = {}
        winniethepooh.force_login(user)
        post_response = winniethepooh.post('/order', data, follow=True)
        order = Order.objects.get(owner=user)
        self.assertContains(post_response, cart.phone_model_item)
        self.assertContains(
            post_response, "<p><b>Order No:</b><span> #{}</span>".
            format(order.pk))
        self.assertContains(
            post_response, "<li>Recipient: {}</li>".
            format(user))
        self.assertContains(
            post_response, "Pick up: To Pick up")

    def test_cancel_order(self):
        """
        Test user can cancel an order.
        """
        (owner, order) = self.generate_review_data()
        response = self.uriel.get('/cancel/{}'.format(order.pk))
        self.assertEqual(response.status_code, 200)
        cancelled_order = CancelledOrder.objects.get(owner=order.owner)
        self.assertEqual(order.quantity, cancelled_order.quantity)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(owner=owner)

    def test_cancel_non_existent_order(self):
        """
        Test that the app handles cancelling of a non existent order.
        """
        response = self.uriel.get('/cancel/12345', follow=True)
        self.assertRedirects(response, '/dashboard')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, 'error')
        s_msg = 'That order does not exist'
        self.assertTrue('{}'.format(s_msg) in message.message)

    def test_disable_cancel_order(self):
        """
        Test the request for disabling cancel order
        """
        (owner, order) = self.generate_review_data()
        data = {'order_id': order.id}
        response = self.client.get("/disable_cancel_order", data)
        msg = str(response.content, 'utf-8')
        self.assertIn(msg, 'Success!')
        order = Order.objects.get(owner=owner)
        self.assertFalse(order.is_cancellable)

    def test_disable_cancel_non_existent_order(self):
        """
        Test the request for disabling cancel order with
             a non existent order
        """
        (owner, order) = self.generate_review_data()
        data = {'order_id': 12345}
        response = self.client.get("/disable_cancel_order", data)
        msg = str(response.content, 'utf-8')
        self.assertIn(msg, 'Order not found')

    def generate_review_data(self, shipping_address=None):
        """Generate data for a review."""
        owner = User.objects.get(email="urieltimanko@example.com")
        OrderStatus.objects.create(status="Pending")
        status = OrderStatus.objects.get(status="Pending")
        address = ShippingAddress.objects.create(
            phone_number="0715557775", country_code=self.code,
            location="Kiambu Road", pickup=True)
        Order.objects.create(
            owner=owner, phone=self.samsung_note_5_rose_gold, status=status,
            quantity=2, total_price=80000, shipping_address=address)
        order = Order.objects.get(owner=owner)
        return (owner, order)
