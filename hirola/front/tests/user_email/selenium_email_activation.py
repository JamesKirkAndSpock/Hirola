from front.tests.base_selenium import *
import time


class InactiveUserRedirect(BaseSeleniumTestCase):

    """Test inactive user is redirected to the right page."""

    def setUp(self):
        super(InactiveUserRedirect, self).setUp()
        self.driver = webdriver.Chrome()
        self.create_country_code()
        self.driver.implicitly_wait(30)
        self.create_inactive_user()

    def test_login_inactive_user(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/login'))
        email_input = driver.find_element_by_name("email")
        email_input.send_keys("timon@gmail.com")
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("secrets")
        submit_button = driver.find_element_by_name("action")
        submit_button.click()
        message = driver.find_element_by_tag_name('b').text
        self.assertEqual(message, 'Hey timon you are almost there!')

    def tearDown(self):
        self.driver.stop_client()
        self.driver.close()
