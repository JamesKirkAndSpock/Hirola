"""Contains front end tests for hotdeals."""
from front.tests.base_selenium import (
    BaseSeleniumTestCase, webdriver, PhoneCategory)


class HotDealLinksTestCase(BaseSeleniumTestCase):
    """Tests hotdeals links redirect to the expected parts of the site."""

    def setUp(self):
        super(HotDealLinksTestCase, self).setUp()
        self.driver = webdriver.Chrome()
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
        self.create_hotdeal()
        self.create_social_media()

    def test_landingpage_hotdeal_link(self):
        """
        Test that that when a hotdeal on the landing page is clicked
            -   it redirects to the hotdeal's page
        """
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.find_element_by_id('money').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/hot_deal/{}/'.
                          format(self.samsung_note_5_rose_gold.pk)))

    def test_breadcrumb_phone_category_link(self):
        """
        Test that on the hotdeal's page
            -   the breadcrumb phone category link is clickable
                and it redirects to the phone category page
        """
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.find_element_by_id('money').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/hot_deal/{}/'.
                          format(self.samsung_note_5_rose_gold.pk)))
        self.driver.find_element_by_link_text(str(self.android)).click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/phone_category/{}/'.
                          format(self.android.pk)))

    def test_breadcrumb_phone_link(self):
        """
        Test that on the hotdeal's page
            -   the breadcrumb phone link is clickable
                and it redirects to the phone profile page
        """
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.find_element_by_id('money').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/hot_deal/{}/'.
                          format(self.samsung_note_5_rose_gold.pk)))
        self.driver.find_element_by_link_text(str(self.samsung_note_5)).click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/profile/{}/'.
                          format(self.samsung_note_5_rose_gold.pk)))

    def test_add_to_cart_button(self):
        """
        Test that on the hotdeal's page
            -   the add to cart button is clickable
                and it redirects to the cart page
        """
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.find_element_by_id('money').click()
        self.driver.find_element_by_id('add-to-cart-button2').click()
        self.assertEqual(self.driver.current_url, '%s%s' %
                         (self.live_server_url, '/before_checkout_anonymous'))

    def test_social_media_links(self):
        """
        Test that on the hotdeal's page
            -   social media links have been rendered
        """
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.find_element_by_id('money').click()
        self.driver.find_element_by_link_text("Facebook").click()
        self.assertEquals(len(self.driver.window_handles), 2)

    def test_categories_rendered(self):
        """
        Test that on the hotdeal's page
            -   categories have been rendered
        """
        categories = ["iPhone", "Android"]
        for category in categories:
            self.driver.get('%s%s' % (self.live_server_url, '/'))
            self.driver.find_element_by_id('money').click()
            self.driver.find_element_by_link_text("{}".format(
                category)).click()
            category_pk = PhoneCategory.objects.get(phone_category=category).pk
            self.assertEqual(
                self.driver.current_url, '%s%s' % (
                    self.live_server_url, '/phone_category/{}/'.format(
                        category_pk)))
            category_pk += 1

    def tearDown(self):
        self.driver.close()
