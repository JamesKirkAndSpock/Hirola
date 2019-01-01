from front.base_test import *
from front.tests.test_users import UserSignupTestCase


class DashboardTemplate(BaseTestCase):

    def setUp(self):
        super(DashboardTemplate, self).setUp()
        user_data = UserSignupTestCase().generate_user_data({})
        response = self.client.post('/signup', user_data)
        html_content = "We have sent you a link to your email to activate your registration"
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
                "phone": self.samsung_j_7.id}
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
            data.append({"stars": i+1, "comments": "Great job guys", "owner": owner.id,
                         "phone": self.iphone_6.id})
        checked_star = (
            "<i class=\"material-icons left checked\">grade</i>\n             "
            "               \n                            "
        )
        unchecked_star = (
            "<i class=\"material-icons left\">grade</i>\n      "
            "                      \n                            "
        )
        checked_counter = 1
        unchecked_counter = 4
        for i in range(5):
            self.elena.post('/admin/front/review/add/', data[i])
            response = self.uriel.get('/dashboard')
            self.assertContains(response, checked_star*(i+1))
            self.assertContains(response, unchecked_star*(4-i))
            Review.objects.get(stars=i+1).delete()

    def test_order_data_get_request(self):
        '''
        Test that if a moves to the dashboard, and that he had made some orders
            - That the order details for his past orders are rendered:
        '''
        (owner, order) = self.generate_review_data()
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, order.phone.phone_name)
        self.assertContains(get_response, "<p><b>Order No.</b><span> #{}</span>".format(order.pk))
        self.assertContains(get_response, "<b>Payment Method</b><span> {}</span>".format(order.payment_method))
        self.assertContains(get_response, "<b>Quantity</b><span> {}</span>".format(order.quantity))
        self.assertContains(get_response, "<b>Total Price</b><span> 80000</span>".format(order.total_price))
        self.assertContains(get_response, "<span> {}</span>".format(order.status))
        self.assertContains(get_response, "<b>Purchase Date </b><span> {}".format(order.date.strftime("%b. ")))
        self.assertContains(get_response, "Recepient: {}".format(owner))
        self.assertContains(get_response, "Location: {}".format(order.get_address.location))
        self.assertContains(get_response, "Pick up: {}".format(order.get_address.pickup))

    def test_order_data_post_request(self):
        '''
        Test that if a moves to the dashboard, and that he had made some orders and he posts something:
            - That the order details for his past orders are rendered:
        '''
        (owner, order) = self.generate_review_data()
        first_name_data = {"first_name": "Britney"}
        post_response = self.uriel.post('/dashboard', first_name_data)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, order.phone.phone_name)
        self.assertContains(post_response, "<p><b>Order No.</b><span> #{}</span>".format(order.pk))
        self.assertContains(post_response, "<b>Payment Method</b><span> {}</span>".format(order.payment_method))
        self.assertContains(post_response, "<b>Quantity</b><span> {}</span>".format(order.quantity))
        self.assertContains(post_response, "<b>Total Price</b><span> 80000</span>".format(order.total_price))
        self.assertContains(post_response, "<span> {}</span>".format(order.status))
        self.assertContains(post_response, "<b>Purchase Date </b><span> {}".format(order.date.strftime("%b. ")))
        self.assertContains(post_response, "Recepient: {}".format(first_name_data["first_name"] + " " + owner.last_name))
        self.assertContains(post_response, "Location: {}".format(order.get_address.location))
        self.assertContains(post_response, "Pick up: {}".format(order.get_address.pickup))

    def test_order_data_with_recepient(self):
        '''
        Test that when you create a recepient for the Shipping Address:
            - That the recepient's name is rendered rather than the owner's name. 
        '''
        (owner, order) = self.generate_review_data()
        shipping_address = ShippingAddress.objects.get(order=order)
        shipping_address.recepient = "Mishael Tchala"
        shipping_address.save()
        get_response = self.uriel.get('/dashboard')
        self.assertContains(get_response, "Recepient: {}".format(order.get_address.recepient))




    def generate_review_data(self, shipping_address=None):
        owner = User.objects.get(email="urieltimanko@example.com")
        PhoneList.objects.create(category=self.iphone, main_image=image('test_image_5.png'),
                                 phone_name="Samsung", currency=self.currency_v, price=25000)
        OrderStatus.objects.create(status="Pending")
        phone = PhoneList.objects.get(phone_name="Samsung")
        status = OrderStatus.objects.get(status="Pending")
        Order.objects.create(
            owner=owner, phone=phone, status=status, quantity=2, total_price=80000)
        order = Order.objects.get(owner=owner)
        ShippingAddress.objects.create(order=order, location="Kiambu Road", pickup="Evergreen Center")
        return (owner, order)
