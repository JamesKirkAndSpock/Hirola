from front.tests.base_selenium import *
from selenium.webdriver.chrome.options import Options
import time


class EmailSentPageLinks(BaseSeleniumTestCase):
    """
    Test that links on the signup page
    behave as expected
    """

    def setUp(self):
        super(EmailSentPageLinks, self).setUp()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.create_country_code()
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.stop_client()
        self.driver.close()


    def test_confirm_email_link(self):
        """Test link redirects to email provider page."""
        self.driver.get('%s%s' % (self.live_server_url, '/signup'))
        self.driver.find_element_by_name('first_name').send_keys('Peter')
        self.driver.find_element_by_name('last_name').send_keys('Ndungu')
        self.driver.find_element_by_class_name('select-wrapper').click()
        self.driver.find_elements_by_tag_name('span')[1].click()
        self.driver.find_element_by_name('phone_number').send_keys('712705422')
        self.driver.find_element_by_name('email').send_keys('ndunguwanyinge@example.com')
        self.driver.find_element_by_name('password1').send_keys('mrndungu2018')
        self.driver.find_element_by_name('password2').send_keys('mrndungu2018')
        self.driver.find_element_by_tag_name('button').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/signup'))
        self.driver.find_element_by_tag_name('button').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.assertEqual(self.driver.current_url,
                         "https://www.google.com/")

    def test_resend_now_link(self):
        """Test resend now link redirects to login page after resending email."""
        self.driver.get('%s%s' % (self.live_server_url, '/signup'))
        self.driver.find_element_by_name('first_name').send_keys('Peter')
        self.driver.find_element_by_name('last_name').send_keys('Ndungu')
        self.driver.find_element_by_class_name('select-wrapper').click()
        self.driver.find_elements_by_tag_name('span')[1].click()
        self.driver.find_element_by_name('phone_number').send_keys('712705422')
        self.driver.find_element_by_name(
            'email').send_keys('ndunguwanyinge@outlook.com')
        self.driver.find_element_by_name('password1').send_keys('mrndungu2018')
        self.driver.find_element_by_name('password2').send_keys('mrndungu2018')
        self.driver.find_element_by_tag_name('button').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/signup'))
        self.driver.find_element_by_link_text('resend now').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/login'))

    def test_change_email(self):
        """Test change email."""
        self.driver.get('%s%s' % (self.live_server_url, '/signup'))
        self.driver.find_element_by_name('first_name').send_keys('Peter')
        self.driver.find_element_by_name('last_name').send_keys('Ndungu')
        self.driver.find_element_by_class_name('select-wrapper').click()
        self.driver.find_elements_by_tag_name('span')[1].click()
        self.driver.find_element_by_name('phone_number').send_keys('712705422')
        self.driver.find_element_by_name(
            'email').send_keys('ndunguwanyinge@outlook.com')
        self.driver.find_element_by_name('password1').send_keys('mrndungu2018')
        self.driver.find_element_by_name('password2').send_keys('mrndungu2018')
        self.driver.find_element_by_tag_name('button').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/signup'))
        self.driver.find_element_by_link_text('change now').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/change_activation_email/ndunguwanyinge@outlook.com/'))
        self.driver.find_element_by_name(
            'email').send_keys('pndungu54@gmail.com')
        self.driver.find_element_by_tag_name('button').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/send_link_to_new_address/ndunguwanyinge@outlook.com/'))
