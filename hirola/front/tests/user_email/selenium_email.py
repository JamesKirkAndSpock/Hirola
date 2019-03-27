"""Contains tests for login page."""
from front.tests.base_selenium import BaseSeleniumTestCase, webdriver


class EmailLogin(BaseSeleniumTestCase):
    '''
    Test that the Login Page functions as expected depending on the email used.
    '''

    def setUp(self):
        super(EmailLogin, self).setUp()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

    def test_login_user_invalid_email(self):
        """Test user cannot login with invalid login."""
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/login'))
        email_input = driver.find_element_by_name("email")
        email_input.send_keys("timonpumba@gmail.com")
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("secret")
        submit_button = driver.find_element_by_name("action")
        submit_button.click()
        error_message = "We cannot find an account with that email address."
        assert error_message in driver.page_source

    def tearDown(self):
        self.driver.close()
