from .base_selenium import *


class Navbar(StaticLiveServerTestCase, TestCase):
    """
    Test that links on the navbar will redirect to the
    page intended
    """

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        super(Navbar, self).setUp()

    def test_about_page_link(self):
        """
        Test that the when a user moves to the home page and clicks on the
        News page link, that the link redirects to the news page.
        """
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("News").click()
        self.assertEqual(driver.current_url, '%s%s' %
                         (self.live_server_url, '/news'))

    def tearDown(self):
        self.driver.close()
