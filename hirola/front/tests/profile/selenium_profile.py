"""Contains tests for the user profile page."""
from front.tests.base_selenium import BaseSeleniumTestCase, webdriver
from selenium.webdriver.chrome.options import Options


class PhoneProfileLink(BaseSeleniumTestCase):
    '''
    Test that buttons, and links on the profile page will redirect to the
    page intended
    '''

    def setUp(self):
        super(PhoneProfileLink, self).setUp()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(30)
        self.create_country_code()
        self.create_phone_category()
        self.create_phone_memory_size()
        self.create_currency()
        self.create_item_icon()
        self.create_color()
        self.create_phone_brand()
        self.create_phone_model()
        self.create_phone_model_list()

    def test_teke_link(self):
        '''
        Test that the teke link redirects to the landing page
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5_rose_gold.pk)
                ))
        driver.find_element_by_id("profile-main-page").click()
        self.assertEqual(
            driver.current_url, '%s%s' % (self.live_server_url, '/')
            )

    def test_iphone_link(self):
        '''
        Test that the iphone link redirects to the phone category
        page for iphones
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5_rose_gold.pk)
                ))
        driver.find_element_by_link_text("Android").click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/phone_category/{}/'.format(
                self.android.pk)
                ))

    def test_phone_link(self):
        '''
        Test that the phone link redirects to the phone page for the specified
        phone.
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/profile/{}/'.format(
            self.samsung_note_5_rose_gold.pk
            )))
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5_rose_gold.pk)
                ))

    def test_faq_link(self):
        '''
        Test that the FAQ link redirects to the help page
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.iphone.pk)))
        driver.find_element_by_link_text("FAQs").click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/help'
            ))

    def test_dashboard_link(self):
        '''
        Test that the dashboard link redirects to the dashboard page for a
        user
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(self.iphone.pk)))
        driver.find_element_by_id("dropdown").click()
        driver.find_element_by_link_text("Login").click()
        self.assertEqual(
            driver.current_url, '%s%s' % (
                self.live_server_url, '/login?next=/dashboard'
                ))

    def test_navbar_teke_link(self):
        '''
        Test that the navbar teke link redirects to the landing page
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.iphone.pk
                )))
        driver.find_element_by_id("base-main-page").click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/'
            ))

    def test_missing_profile(self):
        '''
        Test that when you visit a profile that does not exist:
        - That the user gets a 404 error message that the product
          does not exist
        '''
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/2123764872138/'))
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/error'
            ))

    def test_category_link(self):
        """
        Test that when a user clicks on the category link on
        the breadcrumb
         - That the link redirects to the correct page
        """
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5_rose_gold.pk)
                ))
        driver.find_element_by_link_text("{}".format(self.android)).click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/phone_category/{}/'.format(
                self.android.pk)
                ))

    def test_phone_profile_link(self):
        """
        Test that when a user clicks on the phone profile link on
        the breadcrumb
         - That the link redirects to the same page
        """
        driver = self.driver
        driver.get('%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5.pk)
                ))
        driver.find_element_by_link_text("{}".format(
            self.samsung_note_5)).click()
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/profile/{}/'.format(
                self.samsung_note_5.pk)
                ))

    def tearDown(self):
        self.driver.close()
