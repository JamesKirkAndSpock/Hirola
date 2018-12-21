from .base_selenium import *


class FooterLink(BaseSeleniumTestCase):
    '''
    Test that buttons, and links on the footers will redirect to the page intended
    '''

    def setUp(self):
        super(FooterLink, self).setUp()

    def test_news_link(self):
        '''
        Test that when a user moves to the home page and clicks on the News and Press link:
            - That the link redirects to the news page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("News and Press").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/news'))

    def test_privacy_policy_link(self):
        '''
        Test that when a user moves to the home page and clicks on the Privacy and Policy link:
            - That the link redirects to the privacy and policy page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("Privacy Policy").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/privacy'))

    def test_about_page_link(self):
        '''
        Test that the when a user moves to the home page and clicks on the About Teke page link:
            - That the link redirects to the about page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("About teke").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/about'))

    def test_teke_vs_others_link(self):
        '''
        Test that the when a user moves to the home page and clicks on the teke vs. Others page
        link:
            - That the link redirects to the teke vs. Others page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("teke vs. Others").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/teke_vs_others'))

    def test_footer_faq_link(self):
        '''
        Test that when a user moves to the home page and clicks on the footer FAQs page link:
            - That the the link redirects to the help page
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_id("footer-faqs").click()
        self.assertEqual(driver.current_url, '%s%s' % (self.live_server_url, '/help'))

    def test_buy_category_link(self):
        '''
        Test that when a user moves to the Buy iPhone link and the Buy Android link:
            - That the links redirect to their respective phone category link.
        '''
        categories = ["iPhone", "Android"]
        for category in categories:
            driver = self.driver
            driver.get('%s%s' % (self.live_server_url, '/'))
            driver.find_element_by_link_text("Buy {}".format(category)).click()
            category_pk = PhoneCategory.objects.get(phone_category=category).pk
            self.assertEqual(driver.current_url,
                             '%s%s' % (self.live_server_url,
                                       '/phone_category/{}/'.format(category_pk)))
            category_pk += 1

    def test_social_media_link(self):
        '''
        Test that when a user moves to the Facebook link:
            - That the links opens another window.
        '''
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/'))
        driver.find_element_by_link_text("Facebook").click()
        self.assertEquals(len(driver.window_handles), 2)

    def tearDown(self):
        self.driver.close()
