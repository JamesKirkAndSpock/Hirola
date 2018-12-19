from .base_selenium import *
from front.models import User


class MyOrders(StaticLiveServerTestCase, TestCase):
    '''
    Test that the My Orders Page functions as expected
    '''
    fixtures = ['test_order_data.json']

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        user = User.objects.get(email="timonpumba@gmail.com")
        user.set_password("secret")
        user.save()
        super(MyOrders, self).setUp()

    def login_user(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/login'))
        email_input = driver.find_element_by_name("email")
        email_input.send_keys("timonpumba@gmail.com")
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("secret")
        submit_button = driver.find_element_by_name("action")
        submit_button.click()
        return driver



    def test_order_details_link(self):
        '''
        Test that when a user moves to the order_detail and clicks on the MY ORDERS link:
            - That the link opens up the orders that the user has
        '''
        driver = self.login_user()
        driver.get('%s%s' % (self.live_server_url, '/dashboard'))
        order_link = driver.find_element_by_link_text("MY ORDERS")
        order_link.click()
        order_1 = driver.find_element_by_id("details-1")
        self.assertEqual(order_1.get_attribute('style'), '')
        order_details_link = driver.find_element_by_id("order-details-button")
        order_details_link.click()
        self.assertEqual(order_1.get_attribute('style'), "display: block;")
        order_details_link.click()
        self.assertEqual(order_1.get_attribute('style'), "display: none;")
