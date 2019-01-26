from front.tests.base_selenium import *
import time


class EmailSentPageLinks(BaseSeleniumTestCase):
    """
    Test that links on the signup page
    behave as expected
    """

    def setUp(self):
        super(EmailSentPageLinks, self).setUp()
        self.driver = webdriver.Chrome()
        self.create_country_code()
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.stop_client()
        self.driver.close()

    # def test_confirm_email_link(self):
    #     """Test link redirects to email provider page."""
    #     self.driver.get('%s%s' % (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_name('first_name').send_keys('Peter')
    #     self.driver.find_element_by_name('last_name').send_keys('Ndungu')
    #     self.driver.find_element_by_class_name('select-wrapper').click()
    #     self.driver.find_elements_by_tag_name('span')[1].click()
    #     self.driver.find_element_by_name('phone_number').send_keys('712705422')
    #     self.driver.find_element_by_name('email').send_keys('ndunguwanyinge@gmail.com')
    #     self.driver.find_element_by_name('password1').send_keys('mrndungu2018')
    #     self.driver.find_element_by_name('password2').send_keys('mrndungu2018')
    #     self.driver.find_element_by_tag_name('button').click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_tag_name('button').click()
    #     time.sleep(2)
    #     self.driver.switch_to.window(self.driver.window_handles[1])
    #     self.assertEqual(self.driver.current_url,
    #                      "https://mail.google.com/")

    # def test_resend_now_link(self):
    #     """Test resend now link redirects to login page after resending email."""
    #     self.driver.get('%s%s' % (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_name('first_name').send_keys('Van')
    #     self.driver.find_element_by_name('last_name').send_keys('Bronckhorst')
    #     self.driver.find_element_by_class_name('select-wrapper').click()
    #     self.driver.find_element_by_xpath("//span[text()='+254 Kenya']").click()
    #     self.driver.find_element_by_name('phone_number').send_keys('722000000')
    #     self.driver.find_element_by_name(
    #         'email').send_keys('van@outlook.com')
    #     self.driver.find_element_by_name('password1').send_keys('mrvan2018')
    #     self.driver.find_element_by_name('password2').send_keys('mrvan2018')
    #     self.driver.find_element_by_tag_name('button').click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_link_text('resend now').click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/login'))

    # def test_change_email(self):
    #     """Test change email."""
    #     self.driver.get('%s%s' % (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_name('first_name').send_keys('Van')
    #     self.driver.find_element_by_name('last_name').send_keys('Bronckhorst')
    #     self.driver.find_element_by_class_name('select-wrapper').click()
    #     self.driver.find_element_by_xpath("//span[text()='+254 Kenya']").click()
    #     self.driver.find_element_by_name('phone_number').send_keys('722000000')
    #     self.driver.find_element_by_name(
    #         'email').send_keys('van@outlook.com')
    #     self.driver.find_element_by_name('password1').send_keys('mrvan2018')
    #     self.driver.find_element_by_name('password2').send_keys('mrvan2018')
    #     self.driver.find_element_by_tag_name('button').click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/signup'))
    #     self.driver.find_element_by_link_text('change now').click()
    #     # self.driver.find_element_by_xpath("//a[text()='change now']").click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/change_activation_email/van@outlook.com/'))
    #     self.driver.find_element_by_name(
    #         'email').send_keys('bronck@gmail.com')
    #     self.driver.find_element_by_tag_name('button').click()
    #     self.assertEqual(self.driver.current_url, '%s%s' %
    #                      (self.live_server_url, '/send_link_to_new_address/van@outlook.com/'))
    def tearDown(self):
        self.driver.stop_client()
        self.driver.close()


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
