from front.tests.base_selenium import BaseSeleniumTestCase, webdriver
import time

class SendSupportEmailTestCase(BaseSeleniumTestCase):

    """Test user can send support email."""

    def setUp(self):
        super(SendSupportEmailTestCase, self).setUp()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

    def test_send_support_email(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/help#help-center'))
        name_input = driver.find_element_by_name("name")
        name_input.send_keys("peter")
        email_input = driver.find_element_by_name("email")
        email_input.send_keys("t@gmail.com")
        comment_input = driver.find_element_by_name("comment")
        comment_input.send_keys("I have nothing to say")
        submit_button = driver.find_element_by_name("action")
        submit_button.click()
        time.sleep(20)
        self.assertEqual(driver.current_url, '%s%s' % (
            self.live_server_url, '/help#help-center'))

    def tearDown(self):
        self.driver.stop_client()
        self.driver.close()
