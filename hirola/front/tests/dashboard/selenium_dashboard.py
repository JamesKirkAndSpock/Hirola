"""Contains selenium tests for the My Orders Page."""
from front.tests.base_selenium import (BaseSeleniumTestCase, webdriver)


class MyOrders(BaseSeleniumTestCase):
    '''
    Test that the My Orders Page functions as expected
    '''

    def setUp(self):
        super(MyOrders, self).setUp()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.create_country_code()
        self.create_user()
        self.create_phone_category()
        self.create_phone_memory_size()
        self.create_currency()
        self.create_item_icon()
        self.create_order_status()
        self.create_payment_method()
        self.create_color()
        self.create_phone_brand()
        self.create_phone_model()
        self.create_phone_model_list()
        self.create_shipping_address()

    def login_user(self):
        """Login test user."""
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
        Test that when a user moves to the order_detail and clicks on the
            MY ORDERS link:
            - That the link opens up the orders that the user has
        '''
        self.create_order()
        driver = self.login_user()
        driver.get('%s%s' % (self.live_server_url, '/dashboard'))
        order_link = driver.find_element_by_link_text("MY ORDERS")
        order_link.click()
        order_1 = driver.find_element_by_id("details-{}".format(
            self.order.pk))
        self.assertEqual(order_1.get_attribute('style'), '')
        order_details_link = driver.find_element_by_id("order-details-button")
        order_details_link.click()
        self.assertEqual(order_1.get_attribute('style'), "display: block;")
        order_details_link.click()
        self.assertEqual(order_1.get_attribute('style'), "display: none;")

    def test_dashboard_link_on_dashboard(self):
        """
        Test that when the user clicks on the dashboard link while on the
        dashboard page
            - That they are redirected to the same page
        """
        driver = self.login_user()
        driver.get('%s%s' % (self.live_server_url, '/dashboard'))
        driver.find_element_by_id("last-link").click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/dashboard'))

    def test_confirm_cancel_link(self):
        '''
        Test that when a user moves to the order_detail and clicks on the
            Cancel Order button:
            - That a pop up window appears asking them to confirm the action
        '''
        self.create_order()
        driver = self.login_user()
        driver.get('%s%s' % (self.live_server_url, '/dashboard'))
        driver.find_element_by_link_text("MY ORDERS").click()
        driver.find_element_by_id("order-details-button").click()
        btn = driver.find_element_by_id("cancelOrderBtn")
        btn.click()
        confirm_link = driver.find_element_by_link_text('Confirm')
        confirm_link.click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/cancel/{}'.format(self.order.pk)))

    def test_confirm_expired_order_cancel(self):
        '''
        Test that when a user attempts to cancel an order
            whose window has expire.
            - That they are redirected to the same page
        '''
        self.create_expired_order()
        driver = self.login_user()
        driver.get('%s%s' % (self.live_server_url, '/dashboard'))
        driver.find_element_by_link_text("MY ORDERS").click()
        driver.find_element_by_id("order-details-button").click()
        btn = driver.find_element_by_id("cancelOrderBtn")
        btn.click()
        confirm_link = driver.find_element_by_link_text('Confirm')
        confirm_link.click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/dashboard'))

    def tearDown(self):
        self.driver.close()
