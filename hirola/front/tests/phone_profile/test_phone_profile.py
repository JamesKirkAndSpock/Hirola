"""Contains backend tests for phone profile page."""
import json
from front.base_test import BaseTestCase


class PhoneProfilePageTestCase(BaseTestCase):
    """Tests backend logic for phone profile page."""

    def setUp(self):
        """Set up testing environment."""
        super(PhoneProfilePageTestCase, self).setUp()

    def test_correct_phone_model_rendered(self):
        """
        Test that on the phone profile page
            - The correct phone is being displayed.
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_5_rose_gold.id))
        html = "<p id=\"intro\"><b>Samsung Note 5</b></p>"
        self.assertContains(response, html)

    def test_correct_images_rendered(self):
        """
        Test that on the phone profile page
            - The correct images are rendered in the
              carousel
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_5_rose_gold.id))
        img = "<li id=\"main_image_data_thumb\" data-thumb=\"/media/{}\">".\
            format(self.samsung_note_5_rose_gold.main_image)
        self.assertContains(response, img)
        img_2 = "<img id=\"main_image_src\" src=\"/media/{}\" />".\
            format(self.samsung_note_5_rose_gold.main_image)
        self.assertContains(response, img_2)

    def test_color_selector_options(self):
        """
        Test that on the profile page
            - The color selector options are generated properly
                when viewing the page the first time
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_5_rose_gold.id))
        html = '<option value={} selected>{}</option>'.format(
            self.samsung_note_5_rose_gold.color.id,
            self.samsung_note_5_rose_gold.color)
        self.assertContains(response, html)

    def test_storage_selector_options(self):
        """
        Test that on the profile page
            - The storage selector options are generated properly
                when viewing the page the first time
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_5_rose_gold.id))
        html = '<option value={} selected>{}</option>'.format(
            self.samsung_note_5_rose_gold.size_sku.id,
            self.samsung_note_5_rose_gold.size_sku)
        self.assertContains(response, html)

    def test_quantity_selector_options(self):
        """
        Test that on the profile page
            - The quantity selector options are generated properly
                when viewing the page the first time
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_7.id))
        html = '<option value="1" selected>1</option>'
        self.assertContains(response, html)
        for i in range(2, 4):
            html = '<option value="{}">{}</option>'.format(i, i)
            self.assertContains(response, html)

    def test_phone_price_currency_rendered(self):
        """
        Test that on the profile page
            - The price and currency are properly rendered
        """
        response = self.client.get("/profile/{}/".format(
            self.samsung_note_7.id))
        html = '<h5 id="price" class="green-text">V$ 25,000</h5>'
        self.assertContains(response, html)

    def test_get_sizes(self):
        """
        Test that the get sizes url fetches the appropriate data
        """
        data = {
            'phone_model_id': self.lg_plus.id,
            'id': self.lg_plus_silver.color.id}
        response = self.client.get("/get_sizes", data)
        self.assertEqual(json.loads(response.content)['sizes_length'], 1)

    def test_size_change(self):
        """
        Test that the size change url returns the expected data
        """
        data = {
            'phone_model_id': self.samsung_note_7.id,
            'size_id': self.samsung_note_7_rose_gold.size_sku.id}
        response = self.client.get("/size_change", data)
        self.assertContains(response, 4)
        self.assertContains(response, 25000)
        self.assertContains(response, 'V$')
        self.assertContains(response, self.samsung_note_7_rose_gold.main_image)

    def test_size_change_error(self):
        """
        Test that when the size change url doesn't find the required data.
            - That it returns a json error message
        """
        data = {
            'phone_model_id': self.samsung_note_5.id,
            'size_id': self.any_phone_size.id}
        response = self.client.get("/size_change", data)
        error = {
            "message": "Sorry that phone was not found!"}
        self.assertEqual(json.loads(response.content), error)

    def test_change_quantity_url(self):
        """
        Test that the change quantity url returns the expected data.
        """
        data = {
            'phone_model_id': self.iphone_6_s.id,
            'qty': self.iphone_6_s_rose_gold.quantity,
            'size_id': self.iphone_6_s_rose_gold.size_sku.id,
            'color_id': self.iphone_6_s_rose_gold.color.id}
        response = self.client.get("/quantity_change", data)
        result = {
            "total_cost": "100000",
            "currency": "V$"}
        self.assertEqual(json.loads(response.content), result)

    def test_change_quantity_error(self):
        """
        Test that when the size change url doesn't find the required data.
            - That it returns a json error message
        """
        data = {
            'phone_model_id': self.iphone_6_s.id,
            'qty': self.iphone_6_s_rose_gold.quantity,
            'size_id': self.iphone_6_s_rose_gold.size_sku.id,
            'color_id': self.color_three.id}
        response = self.client.get("/quantity_change", data)
        error = {
            "message": "Sorry that phone was not found!"}
        self.assertEqual(json.loads(response.content), error)

    def test_phone_rendering_order(self):
        """
        Test that on the phone profile page
            - The phone with the lowest price is rendered first
        """
        response = self.client.get("/profile/{}/".format(
            self.lg_plus.id))

        self.assertContains(
            response, "{:,}".format(self.lg_plus_silver_two.price))

    def test_phone_category_phone_rendering_order(self):
        """
        Test that on the phone category page
            - The phone with the lowest price is rendered first
        """
        response = self.client.get("/phone_category/{}/".format(
            self.android.id))
        message = response.context.get('phones')[0]
        self.assertEqual(message, self.samsung_note_5_rose_gold)
