import time
from .base_selenium import *
from selenium.webdriver.chrome.options import Options


class NewsTestCase(BaseSeleniumTestCase):
    """
    Test that links on the navbar will redirect to the
    page intended
    """

    def setUp(self):
        super(NewsTestCase, self).setUp()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.create_news()

    def test_news_page_link(self):
        """
        Test that the when a user moves to the home page and clicks on the
        News page link, that the link redirects to the news page.
        """
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("News and Press").click()
        self.assertEqual(driver.current_url, '%s%s' %
                         (self.live_server_url, '/news'))

    def test_links_redirect_to_news_site(self):
        """
        Test that the when a user clicks on one of the news links it redirects
        them to the story's source.
        """
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("News and Press").click()
        self.assertEqual(driver.current_url, '%s%s' %
                         (self.live_server_url, '/news'))
        driver.find_element_by_link_text("Teke rocks").click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        self.assertEqual(driver.current_url, "https://medium.com/")

    def test_news_page_news_link(self):
        """
        Test that the when a user moves to the home page and clicks on the
        News page link, that the link redirects to the news page.
        """
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("News and Press").click()
        self.assertEqual(driver.current_url, '%s%s' %
                         (self.live_server_url, '/news'))
        driver.find_element_by_link_text("news").click()
        self.assertEqual(driver.current_url, '%s%s' %
                         (self.live_server_url, '/news'))

    def tearDown(self):
        self.driver.close()
