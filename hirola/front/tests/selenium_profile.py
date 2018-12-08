from .base_selenium import *


class PhoneProfileLink(StaticLiveServerTestCase, TestCase):
    '''
    Test that buttons, and links on the profile page will redirect to the
    page intended
    '''
    fixtures = ['test_profile_data.json']

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        super(PhoneProfileLink, self).setUp()

    def test_teke_link(self):
        '''
        Test that the teke link redirects to the landing page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        driver.find_element_by_id("profile-main-page").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/'))

    def test_iphone_link(self):
        '''
        Test that the iphone link redirects to the phone category page for iphones
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        driver.find_element_by_link_text("iPhone").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/phone_category/1/'))

    def test_phone_link(self):
        '''
        Test that the phone link redirects to the phone page for the specified
        phone.
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/profile/1/'))

    def test_faq_link(self):
        '''
        Test that the FAQ link redirects to the help page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        driver.find_element_by_link_text("FAQs").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/help'))

    def test_dashboard_link(self):
        '''
        Test that the dashboard link redirects to the dashboard page for a
        user
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        driver.find_element_by_link_text("My Teke").click()
        self.assertEqual(driver.current_url,
                         '%s%s' % (self.live_server_url, '/login?next=/dashboard'))

    def test_navbar_teke_link(self):
        '''
        Test that the navbar teke link redirects to the landing page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        driver.find_element_by_id("base-main-page").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/'))

    def test_cart_link(self):
        '''
        Test that the cart link on the profile page redirects to the checkout
        page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/1/'))
        element = driver.find_element_by_id("add-to-cart-button")
        driver.find_element_by_id("add-to-cart-button").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/checkout'))

    def test_missing_profile(self):
        '''
        Test that when you visit a profile that does not exist:
        - That the user gets a 404 error message that the product does not exist
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/2/'))
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/error'))

    def tearDown(self):
        self.driver.close()
